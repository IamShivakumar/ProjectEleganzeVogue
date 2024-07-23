from django.contrib import admin
from django.urls import path,include
from . import views
from .views import usersignupView,UserLoginView,homepageview,signout,admindashboard


urlpatterns = [
    path('',homepageview.as_view(),name='homepage'),
    path('Userlogin/',UserLoginView.as_view(),name='userlogin'),
    path('usersignup/',usersignupView.as_view(),name='usersignup'),
    path('verify/',views.emailauth,name='emailverification'),
    path('forgot-password/',views.forgotpassword,name="forgotpassword"),
    path('signout/',signout,name='logout'),
    path('dashboard/',admindashboard,name='dashboard'),
]
