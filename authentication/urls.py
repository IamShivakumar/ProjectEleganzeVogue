from django.contrib import admin
from django.urls import path,include
from . import views
from .views import usersignupView,UserLoginView,homepageview,signout,admindashboard,verifyOTPView,resend_otp,chart_data


urlpatterns = [
    path('',homepageview.as_view(),name='homepage'),
    path('Userlogin/',UserLoginView.as_view(),name='userlogin'),
    path('usersignup/',usersignupView.as_view(),name='usersignup'),
    path('verify-otp/<str:email>/', verifyOTPView.as_view(), name='verify_otp'),
    path('resend-otp/<str:email>/', resend_otp, name='resend_otp'),
    path('verify/',views.emailauth,name='emailverification'),
    path('forgot-password/',views.forgotpassword,name="forgotpassword"),
    path('signout/',signout,name='logout'),
    path('dashboard/',admindashboard,name='dashboard'),
    path('chart-data/', chart_data, name='chart_data')
]
