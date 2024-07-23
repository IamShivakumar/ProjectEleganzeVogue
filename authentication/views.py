from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from users.models import CustomUser
from adminside.models import Order, Order_items
from adminside.models import category, products
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator
import re
import json
from django.db.models import Sum
from django.shortcuts import redirect
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

# Create your views here.


class usersignupView(View):
    template_name = "signup.html"

    def post(self, request):
        print(request.POST)
        if request.user.is_authenticated:
            redirect("homepage")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmPassword = request.POST.get("confirmpassword")
        phone_number = request.POST.get("phone")
        errors = {}
        # Username Validation
        if CustomUser.objects.filter(username=username).exists():
            errors["username"] = "Username already exists"
        elif len(username) == 0:
            print(len(username))
            errors["username"] = "Username should not be empty"

        # email validation
        if CustomUser.objects.filter(email=email).exists():
            errors["email"] = "email already exists try another email"
        elif len(email) == 0:
            errors["email"] = "email field should not be empty"
        elif not self.is_valid_email(email):
            errors["email"] = "Email id is not valid!!!"
        if len(phone_number) < 10:
            errors["phone"] = "Phone number should be 10 digits"
        # Password Validation
        if password != confirmPassword:
            errors["password"] = "Password Mismatch"
        elif len(password) == 0:
            errors["password"] = "Please enter a password"
        if errors:
            return render(request, self.template_name, {"errors": errors})

        # User Creation
        user = CustomUser.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
            phone_number=phone_number,
            password=password,
        )
        user.save()
        print("user is saved")
        messages.success(
            request,
            f"User '{username}' has been created successfully! You can now login.",
        )
        return redirect("userlogin")

    def get(self, request):
        if request.user.is_authenticated:
            redirect("homepage")
        return render(request, self.template_name)

    def is_valid_email(self, email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None


@method_decorator(
    cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch"
)
class UserLoginView(View):
    template_name = "login.html"

    def get(self, request):
        if request.user.is_authenticated and request.user.is_active:
            return redirect("homepage")
        return render(request, self.template_name)

    def post(self, request):
        if request.user.is_authenticated and request.user.is_active:
            return redirect("homepage")

        username = request.POST.get("username")
        password = request.POST.get("password")
        errors = {}

        if not username or not password:
            errors["empty"] = "Please Enter Username and Password!!!!"
        else:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("homepage")
            else:
                errors["invalid"] = "Incorrect Username or Password"

        return render(request, self.template_name, {"errors": errors})


@method_decorator(
    cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch"
)
class homepageview(TemplateView):
    def get(self, request):
        template_name = "homepage.html"
        categories = category.objects.all()
        product = products.objects.get(id=1)
        context = {"categories": categories, "product": product}
        print(product)
        return render(request, template_name, context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="adminlogin")
def admindashboard(request):
    if request.method == "GET":
        if request.user.is_admin:
            order_count = Order.objects.all().count()
            pending_order = Order.objects.filter(status="Pending").count()
            recent_orders = Order.objects.all().order_by("-created_at")
            total_revenue = Order.objects.filter(payment_status ='Paid').aggregate(
                total_sum=Sum("total_price")
            )["total_sum"]
            #Prepare Revenune Data
            revenue_data = Order.objects.filter(payment_status='Paid').values(
                'created_at__date'
            ).annotate(
                total_revenue=Sum('total_price')
            ).order_by('created_at__date')
            revenue_labels = [item['created_at__date'].strftime('%b %Y') for item in revenue_data]
            revenue_values = [float(item['total_revenue']) for item in revenue_data]
            # For Product quanitites
            product_quantities = (
                Order_items.objects.values("product__product_name")
                .annotate(total_quantity=Sum("quantity"))
                .order_by("-total_quantity")
            )
            product_labels = [item['product__product_name'] for item in product_quantities]
            product_values = [item['total_quantity'] for item in product_quantities]

            # Get top 3 selling products
            top_selling_products = product_quantities[:3]
            top_selling_products_list = [
                {'name': item['product__product_name'], 'quantity': item['total_quantity']}
                for item in top_selling_products
            ]
            most_ordered_product = product_quantities.first()
            most_ordered_product = most_ordered_product["product__product_name"]
            active_users = CustomUser.objects.filter(is_active=True).count()
            context = {
                "total_orderCount": order_count,
                "pending_order": pending_order,
                "recent_orders": recent_orders,
                "total_revenue": total_revenue,
                "most_ordered_product": most_ordered_product,
                'active_users':active_users,
                'revenue_data': json.dumps({
                    'labels': revenue_labels,
                    'values': revenue_values
                }),
                'product_quantity_data': json.dumps({
                    'labels': product_labels,
                    'values': product_values
                }),
            }
            return render(request, "dashboard.html", context)
        return redirect("adminlogin")
    else:
        return redirect("adminlogin")


def emailauth(request):
    if request.method == "GET":
        return render(request, "emailverification.html")
    if request.method == "POST":
        email = request.POST.get("email")
        errors = {}
        try:
            user = CustomUser.objects.get(email=email)
            request.session["user_email"] = email
            return render(request, "changepassword.html")
        except CustomUser.DoesNotExist:
            errors["no_email"] = "Email Id does not exists"
            if errors:
                return render(request, "emailverification.html", {"errors": errors})


def changepassword(request):
    if request.method == "POST":
        if not request.session.get("user_email"):
            return redirect("emailverification")

        user = CustomUser.objects.get(email=request.session.get("user_email"))
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        errors = {}
        if not new_password:
            errors["new_password"] = "New password is required"

        if not confirm_password:
            errors["confirm_password"] = "Confirm password is required"

        if new_password != confirm_password:
            errors["confirm_password"] = "Passwords did not match!"

        if errors:
            return render(request, "changepassword.html", {"errors": errors})

        user.set_password(new_password)
        user.save()
        return redirect("userlogin")


def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("homepage")
