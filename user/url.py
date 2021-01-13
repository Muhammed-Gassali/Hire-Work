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
    path('quickview/<int:id>', views.quickview, name="quickview"),
    path('collection', views.collection, name="collection"),
    path('add-to-collection/<int:id>', views.add_to_collection, name="add-to-collection"),
    path('delete-collection/<int:id>', views.delete_collection, name="delete-collection"),










    
]