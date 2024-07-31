from django.contrib import admin
from django.urls import path,include
from .  views import adminlogin,categorylisting,addCategory,editcategory,blockcategory,delete_banner,productlisting,banner_listing,addBanner,addproducts,signout,userlisting,blockuser,editproduct,blockproduct,orderlisting,change_order_status,couponlisting,approve_return,get_quantity,update_sku,generate_pdf,delete_coupon


urlpatterns = [
    path('',adminlogin,name='adminlogin'),
    path('signout',signout,name='signout'),
    #Categories CRUD
    path('categories/',categorylisting,name="categorylisting"),
    path('add-category/',addCategory,name='addcategory'),
    path('editcategory/<int:category_id>/',editcategory,name='editcategory'),
    path('blockcategory/<int:category_id>/',blockcategory,name="blockcategory"),
    
    #Product CRUD
    path('products/',productlisting,name='productlisting'),
    path('add-products/',addproducts,name='addproducts'),
    path('edit-product/<int:product_id>',editproduct,name='editproduct'),
    path('blockproduct/<int:product_id>',blockproduct,name='blockproduct'),
    path('get_quantity/', get_quantity, name='get_quantity'),
    path('update_sku/',update_sku,name='update_sku'),

    #User Crud
    path('user-details/',userlisting,name='userlisting'),
    path('blockuser/<int:user_id>',blockuser,name='blockuser'),

    #Banner Crud
    path('banners/',banner_listing,name='banner_listing'),
    path('add-banner/',addBanner,name='addbanner'),
    path('Delete_banner/<int:banner_id>',delete_banner,name='delete_banner'),
    path('orders/',orderlisting,name='orderlisting'),
    path('change-status/<int:order_id>',change_order_status,name='change_order_status'),
    path('approve-return/',approve_return,name='approveReturn'),
    path('coupons/',couponlisting,name='couponlisting'),
    path('delete_coupon/<int:coupon_id>',delete_coupon,name='delete_coupon'),
    path('generate_pdf/',generate_pdf,name='generate_pdf')
]
