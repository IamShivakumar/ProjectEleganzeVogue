from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.db.models import Sum,F,Q
from django.views import View
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from adminside.models import (
    category,
    products,
    size,
    productImages,
    product_sku,
    cart,
    wishlist,
    Order,
    Order_items,
    coupon
)
from .models import userAddress, CustomUser
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .forms import AddressForm
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

# Create your views here.


@method_decorator(
    cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch"
)
class shoppageview(TemplateView):
    template_name = "shop.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_ids = self.request.GET.getlist('categories')
        size_ids=self.request.GET.getlist('sizes')
        category_ids = [int(id) for id in category_ids]
        size_ids = [int(id) for id in size_ids]
        price_order=self.request.GET.get('price')
        search_query = self.request.GET.get('q', '')
        prod = products.objects.all()
        if category_ids:
            prod=prod.filter(category_id__in=category_ids)
        if size_ids:
            prod=prod.filter(productid__size_id__in=size_ids,productid__quantity__gt=0).distinct()
        if search_query:
            prod= prod.filter(
                Q(product_name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        prod=prod.annotate(
            discounted_price=F('price') - (F('price') * F('discount') / Decimal(100))
        )
        if price_order=='low-to-high':
            prod=prod.order_by('price')
        elif price_order=='high-to-low':
            prod=prod.order_by('-price')
        products_with_sku_count = []
        for product in prod:
            skus = product_sku.objects.filter(product=product)
            sku_count=skus.count()
            total_quantity = skus.aggregate(total=Sum('quantity'))['total'] or 0
            all_out_of_stock = sku_count == 0 or total_quantity == 0
            products_with_sku_count.append(
                {
                    "product": product,
                    "out_of_stock": all_out_of_stock,
                }
            )
        context["products"] = products_with_sku_count
        context["categories"] = category.objects.all()
        context["sizes"] = size.objects.all()
        context["selected_categories"] = category_ids
        context["selected_sizes"] = size_ids
        context["selected_price_order"] = price_order
        context["search_query"]=search_query
        return context


@login_required
def wishlistview(request):
    if request.method == "GET":
        wishlist_products = wishlist.objects.filter(
            user_id=request.user.id
        ).select_related("product")
        for product in wishlist_products:
            print(product.product)
        return render(request, "wishlist.html", {"wishlists": wishlist_products})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def product_detail(request, productid):
    if request.method == "GET":
        product = (
            products.objects.filter(id=productid)
            .prefetch_related("productimage", "productid")
            .first()
        )
        productimage = product.productimage.all()
        sizesid = product_sku.objects.filter(
            product=product,
            quantity__gt=0
        ).values_list('size_id', flat=True).distinct()
        
        sizes = size.objects.filter(id__in=sizesid)
        discounted_price = product.get_discounted_price()
        context = {
            "product": product,
            "productimages": productimage,
            "sizes": sizes,
            "discount_price": discounted_price,
        }
        return render(request, "productdetail.html", context)


@login_required
def cartdetail(request):
    if request.method == "GET":
        userid = request.user.id
        cartdetails = cart.objects.filter(user_id=userid).select_related(
            "product", "size"
        )
        for item in cartdetails:
            item.discounted_price = item.product.get_discounted_price()
            available_qty=product_sku.objects.filter(product_id=item.product,size_id=item.size).first()
            item.available_qty=available_qty.quantity
            print(item.available_qty)
            
        return render(request, "cart.html", {"cartdetails": cartdetails})

@login_required
def addtocart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            productid = int(request.POST.get("product_id"))
            productsize = int(request.POST.get("size"))
            print(productsize)
            product = products.objects.get(id=productid)
            if product:
                if cart.objects.filter(user_id=request.user.id, product_id=productid):
                    return JsonResponse({"status": "Product Already Exists in cart"})
                else:
                    cart.objects.create(
                        user_id=request.user.id,
                        product_id=productid,
                        size_id=productsize,
                    )
                    return JsonResponse(
                        {"status": "Product Has been added to cart successfully"}
                    )
            else:
                return JsonResponse(
                    {"status": "Sorry Currently this product is not available"}
                )
        else:
            return JsonResponse({"status": "Please Login to add the product to cart"})

@login_required
def updatecart(request):
    if request.method == "POST":
        product_id = int(request.POST.get("product_id"))
        if cart.objects.filter(user_id=request.user.id, product_id=product_id):
            product_quantity = int(request.POST.get("quantity"))
            carts = cart.objects.get(product_id=product_id, user_id=request.user.id)
            carts.quantity = product_quantity
            carts.save()
            return JsonResponse({"status": "Updated Successfully"})
    else:
        return redirect("home")

@login_required
def deletecartitem(request, product_id):
    productid = product_id
    userid = request.user.id
    cartitem = cart.objects.get(product_id=productid, user_id=userid)
    cartitem.delete()
    return redirect("cart")

@login_required
def addtowishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            productid = int(request.POST.get("product_id"))
            product = products.objects.get(id=productid)
            if product:
                if wishlist.objects.filter(
                    user_id=request.user.id, product_id=productid
                ):
                    return JsonResponse(
                        {"status": "Product is already available in your wishlist"},
                        status=208,
                    )
                else:
                    wishlist.objects.create(
                        user_id=request.user.id, product_id=productid
                    )
                    return JsonResponse(
                        {"status": "Product has been added to your wishlist"},
                        status=200,
                    )
            else:
                return JsonResponse(
                    {"status": "Sorry Currently this Product is not available"}
                )
        else:
            return JsonResponse(
                {"status": "Please login to add the product to the wishlist"}
            )

@login_required
def deletewishlist(request):
    if request.method == "POST":
        productid = int(request.POST.get("product_id"))
        if wishlist.objects.filter(product_id=productid, user_id=request.user.id):
            wishlistitem = wishlist.objects.get(
                product_id=productid, user_id=request.user.id
            )
            wishlistitem.delete()
            return JsonResponse({"status": "Removed from Wishlist"})
    else:
        return redirect("homepage")

@login_required   
def deleteAddress(request):
    if request.method=='POST':
        addressid=int(request.POST.get("address_id"))
        print("Address id to be removed is :",addressid)
        if userAddress.objects.filter(id=addressid,user_id=request.user.id):
            useraddress=userAddress.objects.get(id=addressid,user_id=request.user.id)
            useraddress.delete()
            return JsonResponse({"status":"Address Has been deleted successfully"})
    else:
        return redirect('homepage')

@login_required
def userdetails(request):
    if request.method == "GET":
        address = userAddress.objects.filter(user_id=request.user.id)
        order=Order.objects.filter(user_id=request.user).order_by('-id')
        wallets=CustomUser.objects.get(id=request.user.id)
        wallet_balance=wallets.wallet_balance
        context={
            'address':address,
            'orders':order,
            'wallet_balance':wallet_balance
        }
        return render(request, "userprofile.html",context)


@login_required
def edituser(request):
    if request.method == "POST":
        user = CustomUser.objects.get(id=request.user.id)
        if user:
            username = request.POST.get("username", "").strip()
            first_name = request.POST.get("first_name", "").strip()
            last_name = request.POST.get("last_name", "").strip()
            email = request.POST.get("email", "").strip()
            phone_number = request.POST.get("phone_number", "").strip()
            errors = {}

        if not username:
            errors["username"] = "Username is required"
        if not first_name:
            errors["first_name"] = "First Name is required"
        if not last_name:
            errors["last_name"] = "Last Name is required"
        if not email:
            errors["email"] = "Email is required"
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors["email"] = "Invalid email!!"

        if phone_number and len(phone_number) != 10:
            errors["phone_number"] = "Invalid phone number!! "

        if errors:
            return JsonResponse({"errors": errors}, status=400)

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone_number
        user.save()
        return JsonResponse({"success": True})

    return redirect('homepage')

@login_required
def changePassword(request):
    if request.method=="POST":
        oldpassword=request.POST.get('old_password')
        new_password1=request.POST.get('new_password1')
        confirmpassword=request.POST.get('new_password2')
        errors={}
        if not oldpassword:
            errors['old_password'] = "Old password is required"
        
        if not new_password1:
            errors['new_password1'] = "New password is required"
        
        if not confirmpassword:
            errors['new_password2'] = "Confirm new password is required"
        
        if new_password1 != confirmpassword:
            errors['new_password2'] = "Passwords did not match!"

        if errors:
            return JsonResponse({'errors': errors}, status=400)
        
        if not request.user.check_password(oldpassword):
            errors['old_password'] = "Incorrect old password"
            return JsonResponse({'errors': errors}, status=400)

        request.user.set_password(new_password1)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return JsonResponse({'message': 'Password updated successfully'}, status=200)
    return redirect('homepage')

@login_required
def generate_referral_code(request):
    user = request.user
    user.generate_referral_code()
    return JsonResponse({'referral_code': user.referral_code})

@login_required
def addaddress(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return JsonResponse({"status": "Address added successfully"})
        else:
            errors = {
                field: [error.message for error in errors]
                for field, errors in form.errors.as_data().items()
            }
            print(errors)
            return JsonResponse({"errors": errors})
    return redirect("homepage")



@login_required
def checkout(request):
    if request.method == "GET":
        addresses = userAddress.objects.filter(user_id=request.user.id)
        cartdetail = cart.objects.filter(user_id=request.user.id).select_related(
            "product"
        )
        totalprice = 0
        cart_items = []
        for item in cartdetail:
            product_stock=product_sku.objects.get(product_id=item.product,size_id=item.size)
            if product_stock.quantity < item.quantity:
                messages.error(request,f"Sorry,the quantity you selected for {item.product.product_name} exceeds the available stock(Stock Left: {product_stock.quantity}).")
                return redirect('cart')
            discounted_price = item.product.get_discounted_price()
            item_total_price = discounted_price * item.quantity
            totalprice += item_total_price
            cart_items.append(
                {
                    "product": item.product,
                    "quantity": item.quantity,
                    "size": item.size,
                    "discounted_price": discounted_price,
                    "item_total_price": item_total_price,
                }
            )

        return render(
            request,
            "checkout.html",
            {
                "addresses": addresses,
                "cart_items": cart_items,
                "totalprice": totalprice,
            },
        )

@login_required
def placeorder(request):
    if request.method=="POST":
        new_order=Order()
        if not request.POST.get('selected_address'): 
            messages.error(request,"Please Add Delivery Address")
            return redirect('checkout')
        address_id=int(request.POST.get('selected_address'))
        selected_adddress=userAddress.objects.get(id=address_id)
        new_order.address_name=selected_adddress.name
        new_order.address_house_no=selected_adddress.house_no
        new_order.address_street=selected_adddress.street
        new_order.address_state=selected_adddress.state
        new_order.address_city=selected_adddress.city
        new_order.address_pincode=selected_adddress.pincode
        new_order.user=request.user
        if not request.POST.get('payment_method'): 
            messages.error(request,"Please select the payment method")
            return redirect('checkout')
        if request.POST.get('payment_id'):
            new_order.payment_status='Paid'
            new_order.payment_id=request.POST.get('payment_id')
        new_order.payment_mode=request.POST.get('payment_method')
        cartitem=cart.objects.filter(user_id=request.user).select_related('product')
        total_price=request.POST.get('total_price')
        cart_total_price=0
        for item in cartitem:
            product_stock=product_sku.objects.get(product_id=item.product,size_id=item.size)
            if product_stock.quantity < item.quantity:
                messages.error(request,f"Sorry,the quantity you selected for {item.product.product_name} exceeds the available stock(Stock Left: {product_stock.quantity}).")
                return redirect('cart')
            cart_total_price = cart_total_price + item.product.get_discounted_price() * item.quantity
        new_order.total_price=total_price
        new_order.save()
        #--------------------- Adding to the Order item-------------------------
        for items in cartitem:
            Order_items.objects.create(
                order=new_order,
                product= items.product,
                quantity=items.quantity,
                size=items.size,
                total_price= items.product.get_discounted_price() * items.quantity
            )
        # --------------Clear Product Quantity from the table------------------------
            orderedproduct=product_sku.objects.filter(product_id=items.product.id,size_id=items.size.id).first()
            orderedproduct.quantity= orderedproduct.quantity - item.quantity
            orderedproduct.save()
        #-------- Clear Users Cart Items-------------#
        cart.objects.filter(user_id=request.user).delete()
        print("Order Has been placed Successfully")
        messages.success(request,"Order has been placed successfully")
    return redirect('homepage')

def cancelproduct(request):
    if request.method=="POST":
        order_id=int(request.POST.get('order_id'))
        product_id=int(request.POST.get('product_id'))
        try:
            orderitem=Order_items.objects.get(order_id=order_id,product_id=product_id)
            #----------------Refund the amount for cancellation and changing the status to Cancelled-------------------
            orderitem.order.user.wallet_balance+=orderitem.total_price
            orderitem.order.user.save()
            orderitem.status="Cancelled"
            orderitem.save()
            #----------------Restocking the Stock after cancellation-------------------
            stock=product_sku.objects.get(product_id=product_id,size=orderitem.size)
            stock.quantity+=orderitem.quantity
            stock.save()
            order_items=Order_items.objects.filter(order_id=order_id)
            if all(item.status=="Cancelled" for item in order_items):
                orderitem.order.status="Cancelled"
                orderitem.order.save()
            return JsonResponse({'status':"Product has been Cancelled"})
        except Order_items.DoesNotExist:
            return JsonResponse({'status':"Product not Found"})
    else:
        return redirect('homepage')
    
def returnproduct(request):
    if request.method=="POST":
        order_id=int(request.POST.get('order_id'))
        product_id=int(request.POST.get('product_id'))
        try:
            orderitem=Order_items.objects.get(order_id=order_id,product_id=product_id)
            orderitem.status="Return Requested"
            orderitem.save()
            order_items=Order_items.objects.filter(order_id=order_id)
            if all(item.status=="Return Requested" for item in order_items):
                order=Order.objects.get(id=order_id)
                order.status="Return Requested"
                order.save()
            return JsonResponse({'status':"Sent Request For Returning the Product"})
        except Order_items.DoesNotExist:
            return JsonResponse({'status':"Product not Found"})
    else:
        return redirect('homepage')

def cancelOrder(request):
    if request.method=="POST":
        print(request.POST.get('order_id'))
        order_id=int(request.POST.get('order_id'))
        try:
            order=Order.objects.get(id=order_id,user_id=request.user)
            order_items=Order_items.objects.filter(order_id=order_id)
            order.user.wallet_balance+=order.total_price
            order.user.save()
            order.status="Cancelled"
            for item in order_items:
                if not item.status=="Cancelled":
                    stock=product_sku.objects.get(product=item.product,size=item.size)
                    stock.quantity+=item.quantity
                    stock.save()
                    item.status="Cancelled"
                    item.save()
            order.save()
            return JsonResponse({'status':"Order has been Cancelled"})
        except Order.DoesNotExist:
            return JsonResponse({'status':"Order not found"})
    else:
        return redirect('homepage')

@login_required
def orderDetail(request,orderid):
    if request.method=="GET":
        order=Order.objects.get(id=orderid)
        orderitem=Order_items.objects.filter(order_id=orderid)
        context={
            'order':order,
            'order_item':orderitem
        }
        return render(request,'order_detail.html',context)
    
def applyCoupon(request):
    if request.method=="POST":
        coupon_code=request.POST.get('coupon_code')
        total_price=request.POST.get('total_price')
        try:
            coupons=coupon.objects.get(code=coupon_code)
            discount=coupons.discount
            discounted_price=float(total_price)-(float(total_price)*discount/100)
            response={
                'status':'success',
                'discounted_price':discounted_price,
                'discount':discount,
                'coupon_code':coupon_code
            }
        except coupon.DoesNotExist:
            response={
                'status':'fail',
                'message':'Invalid Coupon Code'
            } 
        return JsonResponse(response)
    
def download_invoice(request, order_id):
    order = Order.objects.get(id=order_id)

    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    # Create the PDF object, using the response object as its "file."
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']

    # Title and Subtitle
    elements = []
    elements.append(Paragraph("INVOICE", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Order # {order.id}", subtitle_style))
    elements.append(Spacer(1, 12))

    # Customer Details
    customer_info = [
        ["Username:", order.user.username],
        ["Email:", order.user.email],
        ["Phone:", order.user.phone_number],
        ["Address:", f"{order.address_name},{order.address_house_no},{order.address_street},{order.address_state},{order.address_city},{order.address_pincode}"],
        ["Order Date:", order.created_at.strftime("%d-%m-%Y")],
    ]
    table = Table(customer_info, hAlign='LEFT')
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Order Details
    elements.append(Paragraph("Order Details", styles['Heading3']))
    order_data = [["Product", "Quantity", "Price"]]
    for item in order.orderItems.all():
        total_item_price=item.quantity * item.product.get_discounted_price()
        order_data.append([item.product.product_name, item.quantity, f"₹{total_item_price}"]) 

    order_table = Table(order_data, hAlign='LEFT')
    order_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(order_table)
    elements.append(Spacer(1, 12))

    # Total Amount
    total_price = f"Total Price: ₹{order.total_price}"
    elements.append(Paragraph(total_price, styles['Heading3']))
    elements.append(Spacer(1, 12))

    # Footer
    elements.append(Paragraph("Thank you for your purchase!", styles['Center']))

    # Build the PDF
    doc.build(elements)

    return response