from django.contrib import admin
from django.urls import path,include
from .views import shoppageview,product_detail,cartdetail,addtocart,userdetails,deletecartitem,addtowishlist,checkout,updatecart,wishlistview,deletewishlist,addaddress,edituser,changePassword,deleteAddress,placeorder,orderDetail,cancelproduct,cancelOrder,applyCoupon,returnproduct,generate_referral_code,download_invoice


urlpatterns = [
    path('shop/',shoppageview.as_view(),name='shop'),
    path('wishlist/',wishlistview,name='wishlist'),
    path('product_detail/<int:productid>',product_detail,name='productdetail'),
    path('checkout/',checkout,name='checkout'),


    path('cart/',cartdetail,name='cart'),
    path('add-to-cart',addtocart,name='addcart'),
    path('update-cart',updatecart,name='updatecart'),
    path('deleteCart/<int:product_id>/',deletecartitem,name='deletecartitem'),

    path('userdetail/',userdetails,name='userdetail'),
    path('edit-user/',edituser,name='edituser'),

    path('addaddress/',addaddress,name='addaddress'),
    path('delete-address',deleteAddress,name="deleteaddresss"),
    path('changepassword/',changePassword,name='changepassword'),

    path('add-to-wishlist',addtowishlist,name='addwishlist'),
    path('delete-wishlist',deletewishlist,name='deletewishlist'),

    path('place-order',placeorder,name='placeorder'),
    path('order_detail/<int:orderid>',orderDetail,name='orderdetail'),
    path('cancel-product',cancelproduct,name="cancelproduct"),
    path('return-product',returnproduct,name="returnproduct"),

    path('cancel-order',cancelOrder,name='cancelorder'),

    path('apply-coupon/',applyCoupon,name='applycoupon'),
    path('generate_referral_code/',generate_referral_code,name='generate_referral_code'),
    path('download_invoice/<int:order_id>',download_invoice,name='download_invoice')
    ]