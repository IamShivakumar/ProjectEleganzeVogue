from django.http import JsonResponse,HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from django.db.models import Sum
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from users.models import CustomUser
from adminside.models import category, size, products, product_sku, productImages,Order,Order_items,coupon,banners
from .forms import CouponForm
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.http import require_POST
from django.db.models import F


# Create your views here.
# ----------------------------------------Admin Authentication--------------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogin(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect("dashboard")
        else:
            return render(request, "adminlogin.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = CustomUser.objects.filter(username=username)
        print(username)
        errors = {}
        if not username or not password:
            errors["empty"] = "Above Fields should not be Empty!!!!"
        else:
            user = authenticate(username=username, password=password)
            print(user, "authenticated")
            if user:
                if user.is_admin:
                    login(request, user)
                    # request.session['username']=username
                    print(f"Username is{username}")
                    return redirect("dashboard")
                else:
                    return redirect("adminlogin")
            else:
                errors["invalid"] = "Incorrect Username or Password"
        if errors:
            return render(request, "adminlogin.html", {"errors": errors})
        else:
            response = render(request, "adminlogin.html")
            return response
    else:
        return render(request, "adminlogin.html")


def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("adminlogin")


# ----------------- Category CRUD Operations-------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="adminlogin")
@user_passes_test(lambda u :u.is_admin)
def addCategory(request):
    if request.method == "GET":
        return render(request, "addcategory.html")

    if request.method == "POST":
        category_name = request.POST.get("category_name")
        discount=request.POST.get("discount")
        category_image = request.FILES.get("category_image")
        status = request.POST.get("status")
        errors = {}
        if status:
            is_active = True
        else:
            is_active = False
        if len(category_name) == 0:
            errors["category_name"] = "Category Name should Not be empty"
        if errors:
            return render(request, "addcategory.html", {"errors": errors})
        else:
            category_create = category.objects.create(
                category_name=category_name, is_active=is_active,discount=discount
            )
            if category_image:
                category_create.category_image = category_image
            category_create.save()
            return redirect("categorylisting")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="adminlogin")
@user_passes_test(lambda u :u.is_admin)
def categorylisting(request):
    if request.method == "GET":
        category_data = category.objects.all()
        return render(request, "categorylisting.html", {"category": category_data})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="adminlogin")
@user_passes_test(lambda u :u.is_admin)
def editcategory(request, category_id):
    if request.method == "GET":
        categories = category.objects.get(id=category_id)
        return render(request, "editcategory.html", {"category": categories})
    if request.method == "POST":
        categories = category.objects.get(id=category_id)
        category_name = request.POST.get("category_name")
        discount=request.POST.get("discount")
        if not category_name.strip():
            # If the category name is empty, render the form with an error message
            return render(
                request,
                "editcategory.html",
                {"category": categories, "error": "Category name cannot be empty."},
            )
        categories.category_name = category_name
        categories.discount=discount
        categories.is_active = request.POST.get("status")
        if "category_images" in request.FILES:
            categories.category_image = request.FILES.get("category_image")
        categories.save()
        return redirect("categorylisting")
    
@login_required(login_url="adminlogin")
@user_passes_test(lambda u :u.is_admin)
def blockcategory(request, category_id):
    categories = category.objects.get(id=category_id)
    categories.is_active = False
    categories.save()
    return redirect("categorylisting")


# ---------------------------------------------Product CRUD Operations----------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="adminlogin")
@user_passes_test(lambda u :u.is_admin)
def productlisting(request):
    if request.method == "GET":
        all_product = (
            products.objects.select_related("category")
            .only(
                "id",
                "product_name",
                "price",
                "description",
                "is_active",
                "category__category_name",
                "discount",
                "primary_image",
            )
            .all().order_by('-id')
        )
        sizes=size.objects.all()
        # print(all_product)
        return render(request, "productlisting.html", {"products": all_product,'sizes':sizes})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="adminlogin")
@user_passes_test(lambda u :u.is_admin)
def addproducts(request):
    sizes = size.objects.all()
    categories = category.objects.all()
    context = {"sizes": sizes, "categories": categories}
    if request.method == "GET":
        return render(request, "add-product.html", context)
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        price = float(request.POST.get("price"))
        description = request.POST.get("description")
        is_active = True if request.POST.get("status") else False
        category_id = request.POST.get("category")
        discount = request.POST.get("discount")
        quantity=request.POST.get("quantity")
        primary_image = request.FILES.get("primary_image")
        other_productimages = request.FILES.getlist("other-images")
        selected_sizes = request.POST.getlist("size")
        errors = {}
        if len(product_name) == 0:
            errors["productname"] = "Please enter product name!!! "
        if len(str(price)) == 0:
            errors["price"] = "Please give a price for the product!!!"
        if len(description) == 0:
            errors["description"] = "Please give a description for the product!!!"
        if errors:
            context.update({"errors": errors})
            return render(request, "add-product.html", context)
        if not discount:
            discount = 0
        category_obj=category.objects.get(id=category_id)
        category_discount=category_obj.discount
        final_price=price-(price * category_discount/100)

        new_product,created = products.objects.get_or_create(
            product_name=product_name,
            defaults={
            'price':final_price,
            'description':description,
            'is_active':is_active,
            'category_id':category_id,
            'discount':discount,
            }
        )
        if not created:
            errors['product_exists']="Product Already Available"

        if primary_image:
            print(primary_image)
            new_product.primary_image = primary_image
        new_product.save()

        for size_id in selected_sizes:
                sizes = size.objects.get(id=size_id)
                productsku,created=product_sku.objects.get_or_create(product=new_product, size=sizes,
                                                defaults= {'quantity':quantity})
                if not created:
                    productsku.quantity=F('quantity')+int(quantity)
                    productsku.save()
                    print("product sku addded")
        product_images_to_create = []
        for image in other_productimages:
            if image:
                print(image)
                new_image = productImages(product=new_product, image=image)
                product_images_to_create.append(new_image)
        # Bulk create all the product images
        productImages.objects.bulk_create(product_images_to_create)
        return redirect("productlisting")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="adminlogin")
@user_passes_test(lambda u :u.is_admin)
def editproduct(request, product_id):
    sizes = size.objects.all()
    categories = category.objects.all()
    context = {"sizes": sizes, "categories": categories}
    if request.method == "GET":
        product = products.objects.get(id=product_id)
        print(product)
        context.update({"product": product})
        return render(request, "editproduct.html", context)
    if request.method == "POST":
        product = products.objects.get(id=product_id)
        product_name = request.POST.get("product_name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        product.is_active = request.POST.get("status")
        product.category_id = request.POST.get("category")
        discount = request.POST.get("discount")
        primary_image = request.FILES.get("primary_image")
        selected_sizes = request.POST.getlist("size")
        errors = {}
        if len(product_name) == 0:
            errors["productname"] = "Please enter product name!!! "
        if len(str(price)) == 0:
            errors["price"] = "Please give a price for the product!!!"
        if len(description) == 0:
            errors["description"] = "Please give a description for the product!!!"
        if not discount:
            discount = 0
        if errors:
            context.update(errors)
            return render(request, "editproduct.html", context)


        product.product_name = product_name
        product.price = price
        product.description = description
        product.discount = discount
        if "primary_image" in request.FILES:
            product.primary_image = primary_image
        product.save()
        return redirect("productlisting")

@user_passes_test(lambda u :u.is_admin)
def blockproduct(request, product_id):
    product = products.objects.get(id=product_id)
    product.is_active = False
    product.save()
    return redirect("productlisting")

@user_passes_test(lambda u :u.is_admin)
def get_quantity(request):
    if request.method=="GET":
        product_id= request.GET.get('product_id')
        size_id=request.GET.get('size_id')
        try:
            product_stock = product_sku.objects.get(product_id=product_id, size=size_id)
            quantity = product_stock.quantity
        except product_sku.DoesNotExist:
            quantity=0
        return JsonResponse({'quantity': quantity})
    
@user_passes_test(lambda u :u.is_admin)
def update_sku(request):
    if request.method=='POST':
        product_id=request.POST.get('product_id')
        size_id=request.POST.get('size')
        quantity=request.POST.get('quantity')
        try:
            stock=product_sku.objects.get(product_id=product_id,size_id=size_id)
            if stock:
                stock.quantity=quantity
                stock.save()
                return redirect('productlisting')
        except product_sku.DoesNotExist:
            product_sku.objects.create(product_id=product_id,size_id=size_id,quantity=quantity)
            return redirect('productlisting')
        


# -------------------------------User Listing-------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="adminlogin")
@user_passes_test(lambda u :u.is_admin)
def userlisting(request):
    if request.method == "GET":
        user = CustomUser.objects.all()
        return render(request, "userdetails.html", {"users": user})

@user_passes_test(lambda u :u.is_admin)
def blockuser(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True  
    user.save()
    return redirect("userlisting")
# ----------------------------------------------------------------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="adminlogin")
@user_passes_test(lambda u :u.is_admin)
def banner_listing(request):
    if request.method == "GET":
        banner_data = banners.objects.all()
        return render(request, "bannerlisting.html", {"banners": banner_data})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="adminlogin")
@user_passes_test(lambda u :u.is_admin)
def addBanner(request):
    if request.method == "GET":
        return render(request, "addbanner.html")
    if request.method=="POST":
        banner_title = request.POST.get("banner_title")
        description=request.POST.get("description")
        banner_image = request.FILES.get("banner_image")
        errors = {}
        if len(banner_title) == 0:
            errors["banner_title"] = "Banner title should Not be empty"
        if errors:
            return render(request, "addbanner.html", {"errors": errors})
        else:
            banner_create = banners.objects.create(
                title=banner_title,description=description
            )
            if banner_image:
                banner_create.banner_image = banner_image
            banner_create.save()
            return redirect("banner_listing")

@login_required(login_url="adminlogin")
@user_passes_test(lambda u :u.is_admin)
def delete_banner(request,banner_id):
    try:
        banner=banners.objects.get(id=banner_id)
        banner.delete()
    except banners.DoesNotExist:
        pass
    return redirect('banner_listing')
    
# ----------------------------------------------------------------------------------


@login_required(login_url="adminlogin")
@user_passes_test(lambda u :u.is_admin)
def orderlisting(request):
    if request.method=="GET":
        orders=Order.objects.all().order_by('-id')
        status_choices= Order.order_status
        orders_with_items = []
        for order in orders:
            items = order.orderItems.all()
            orders_with_items.append({
                'order': order,
                'items': items,
        })    
    context = {
        'orders_with_items': orders_with_items,
        'status_choices': status_choices,
    }
    return render(request,"orderlisting.html", context)

@login_required(login_url="adminlogin")
@user_passes_test(lambda u :u.is_admin)
def change_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items=Order_items.objects.filter(order_id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.order_status).keys():
            if new_status =="Delivered":
                order.payment_status="Paid"
            order.status = new_status
            order.save()
            for items in order_items:
                items.status=new_status
                items.save()                
            messages.success(request, 'Order status updated successfully.')
        else:
            messages.error(request, 'Invalid status selected.')
    return redirect('orderlisting')

@login_required(login_url="adminlogin")
@csrf_exempt
@require_POST
def approve_return(request):
    order_id= int(request.POST.get('order_id'))
    product_id=int(request.POST.get('product_id'))
    order_status=request.POST.get('status')
    try:
        order_item=Order_items.objects.get(order_id=order_id,product_id=product_id)
        if order_status=="Returned":
            order_item.order.user.wallet_balance += order_item.total_price
            order_item.order.user.save()
        order_item.status=order_status
        order_item.save()
        print("Amount After refund",order_item.order.user.wallet_balance)
        order_items=Order_items.objects.filter(order_id=order_id)
        if all(item.status in ["Return Approved","Returned"] for item in order_items):
            order=Order.objects.get(id=order_id)
            order.status="Return Approved" if all(item.status == "Return Approved" for item in order_items) else "Returned"
            order.save()
        return JsonResponse({'success':'Return Approved'})
    except Order_items.DoesNotExist:
        return JsonResponse({'error': 'Order item not found'})
#-----------------------------------------------------------------------------
@login_required(login_url="adminlogin")
@user_passes_test(lambda u :u.is_admin)
def couponlisting(request):
    if request.method=="GET":
        coupons=coupon.objects.all()
        return render(request,'couponlisting.html',{'coupons':coupons})
    
    if request.method=='POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': True})
        else:
            errors = {field: [str(error) for error in form.errors[field]] for field in form.errors}
            print(errors)
            return JsonResponse({"status":False,"errors": errors})
        
@login_required(login_url="adminlogin")
@user_passes_test(lambda u :u.is_admin)
def delete_coupon(request,coupon_id):
    try:
        coupons=coupon.objects.get(id=coupon_id)
        coupons.delete()
    except coupon.DoesNotExist:
        pass
    return redirect('couponlisting')
        
#--------------------------------PDF Generation---------------------------------------------
def generate_pdf(request):
    report_type= request.GET.get('reportType')
    from_date= request.GET.get('fromDate')
    to_date=request.GET.get('toDate')
    orders = Order.objects.none()
    if report_type=="daily":
        orders=Order.objects.filter(created_at__date=datetime.today().date())
    elif report_type=="monthly":
        orders= Order.objects.filter(created_at__month=datetime.today().month, created_at__year=datetime.today().year)
    elif report_type=="monthly":
        orders = Order.objects.filter(created_at__year=datetime.today().year)
    elif report_type == 'custom':
        orders = Order.objects.filter(created_at__range=[from_date, to_date])
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
# Table Title
    p.setFont("Helvetica-Bold",20)
    p.drawString(30,height-40,"Sales Report")

    #Tabel Headers
    p.setFont("Helvetica-Bold", 12)
    p.drawString(30, height - 80, "Order ID")
    p.drawString(100, height - 80, "Products")
    p.drawString(250, height - 80, "Quantity")
    p.drawString(320, height - 80, "Order Date")
    p.drawString(420, height - 80, "Payment Method")
    p.drawString(520, height - 80, "Total Price")
    # Table content
    y = height - 100
    total_revenue = 0
    for order in orders:
        y -= 20
        p.setFont("Helvetica", 10)
        p.drawString(30, y, str(order.id))
        # products = "\n".join([f"{item.product.product_name} ({item.quantity})" for item in order.orderItems.all()])
        # p.drawString(100, y, products)
        p.drawString(320, y, order.created_at.strftime("%Y-%m-%d"))
        p.drawString(420, y, order.payment_mode)
        p.drawString(520, y, f"₹{order.total_price}")
        total_revenue += order.total_price
        for item in order.orderItems.all():
            p.drawString(100, y, item.product.product_name)
            p.drawString(250, y, str(item.quantity))
            y -= 15
        # Check if we need to create a new page
            if y <= 40:
                p.showPage()
                y = height - 40

    # Total Revenue
    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(30, y, "Total Revenue: ")
    p.drawString(150, y, f"₹ {total_revenue}")

    # Save the PDF
    p.showPage()
    p.save()
    buffer.seek(0)

    # Return the PDF as a response
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
    return response
