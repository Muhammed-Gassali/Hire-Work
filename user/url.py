from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.common_home, name="common-home"),
    path('seeker-login', views.seeker_login, name="seeker-login"),
    path('customer-login', views.customer_login, name="customer-login"),
    path('customer-register', views.customer_register, name="customer-register"),
    path('otp-login', views.otp_login, name="otp-login"),
    path('confirm-otp', views.confirm_otp, name="confirm-otp"),
    path('customer-homepage', views.customer_homepage, name="customer-homepage"),
    path('registered-customer-homepage', views.registered_customer_homepage, name="registered-customer-homepage"),
    path('registered-customer-logout', views.registered_customer_logout, name="registered-customer-logout"),
    path('customer-profile', views.customer_profile, name="customer-profile"),
    path('edit-profile', views.edit_profile, name="edit-profile"),
    path('quickview', views.quickview, name="quickview"),







    
]