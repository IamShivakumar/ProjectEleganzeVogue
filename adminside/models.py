from django.db import models
from users.models import CustomUser,userAddress
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal


# Create your models here.
class category(models.Model):
    category_name=models.CharField(max_length=50)
    category_image=models.ImageField(upload_to='category_images',default='null',null=True,blank=True)
    is_active=models.BooleanField(default=True)
    discount=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table="categories"

class size(models.Model):
    size_code=models.CharField(max_length=5)
    size_description=models.CharField(max_length=50)

    class Meta:
        db_table="size"

class products(models.Model):
    product_name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    description=models.TextField()
    is_active=models.BooleanField(default=True)
    category=models.ForeignKey(category,on_delete=models.CASCADE,related_name='category')
    discount=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,default=0)
    primary_image=models.ImageField(upload_to='product_images',default='null',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table="product_detail"

    def get_discounted_price(self):
        if self.discount:
            discount_value = self.price * (Decimal(self.discount) / Decimal(100))
            discounted_price = self.price - discount_value
            return round(discounted_price,2)
        return self.price

class productImages(models.Model):
    product=models.ForeignKey(products,on_delete=models.CASCADE,related_name='productimage')
    image=models.ImageField(upload_to="product_images",default='null',null=True,blank=True)

    class Meta:
        db_table="product_images"

class product_sku(models.Model):
    product=models.ForeignKey(products,on_delete=models.CASCADE,related_name='productid')
    size=models.ForeignKey(size,on_delete=models.CASCADE,related_name='productsize')
    quantity=models.IntegerField(null=True,default=1)
    
    class Meta:
        db_table="product_sku"

class cart(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='usercart')
    product=models.ForeignKey(products,on_delete=models.CASCADE,related_name='cartproduct')
    size=models.ForeignKey(size,on_delete=models.CASCADE,related_name='cartproductsize')
    quantity=models.SmallIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table="cart_details"

class wishlist(models.Model):
        user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='userwishlist')
        product=models.ForeignKey(products,on_delete=models.CASCADE,related_name='productwishlist')
        created_at=models.DateTimeField(auto_now_add=True)
        modified_at=models.DateTimeField(auto_now=True)

        class Meta:
            db_table="Wishlist"

class Order(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='userOrder')
    address=models.ForeignKey(userAddress,on_delete=models.SET_NULL,null=True,related_name='orderAddress')
    payment_mode=models.CharField(max_length=150, null=False)
    payment_id=models.CharField(max_length=150,null=True)
    pay_status=(('Pending','Pending'),('Paid','Paid'))
    total_price=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    order_status=(
        ('Pending','Pending'),
        ('Shipped','Shipped'),
        ('Out for Delivery','Out for Delivery'),
        ('Cancelled','Cancelled'),
        ('Delivered','Delivered'),
        ('Request Return', 'Request Return'),
        ('Return Approved', 'Return Approved'),
        ('Returned','Returned')
    )
    status=models.CharField(max_length=150,choices=order_status,default='Pending')
    payment_status=models.CharField(max_length=150,choices=pay_status,default='Pending')
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    address_name=models.CharField(max_length=150,null=True,blank=True)
    address_house_no=models.CharField(max_length=10,null=True,blank=True)
    address_street=models.CharField(max_length=50,null=True,blank=True)
    address_state=models.CharField(max_length=50,null=True,blank=True)
    address_city=models.CharField(max_length=100,null=True,blank=True)
    address_pincode=models.BigIntegerField(null=True,blank=True)
    

    class Meta:
        db_table='Order_details'

class Order_items(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='orderItems')
    product=models.ForeignKey(products,on_delete=models.CASCADE,related_name='orderproducts')
    quantity=models.SmallIntegerField(null=False,default=1)
    size=models.ForeignKey(size,on_delete=models.SET_NULL,null=True,related_name='orderedproductsize')
    total_price=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    status_choices = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Cancelled', 'Cancelled'),
        ('Delivered', 'Delivered'),
        ('Request Return', 'Request Return'),
        ('Return Approved', 'Return Approved'),
        ('Returned','Returned')
    )
    status = models.CharField(max_length=150, choices=status_choices, default='Pending')
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table="order_items"


class coupon(models.Model):
    code=models.CharField(max_length=100,unique=True,null=False)
    description=models.CharField(max_length=100,null=False)
    discount=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=False,default=0)

    class Meta:
        db_table="Coupons"

class banners(models.Model):
    title=models.CharField(max_length=200,null=False)
    description=models.TextField()
    banner_image=models.ImageField(upload_to='banner_images',default='null',null=True,blank=True)

    class Meta:
        db_table="Banner"