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
    path('order/', views.order_verify, name="order"),
    path('order-confirmation', views.order_confirmation, name="order-confirmation"),
    path('contact', views.contact, name="contact"),
    path('customer-order-cancel/<int:id>', views.customer_order_cancel, name="customer-order-cancel"),
    path('customer-feedback/<int:id>', views.customer_feedback, name="customer-feedback"),
    path('razorpay-confirm/', views.razorpay_confirm, name="razorpay-confirm"),








    path('rest', views.rest.as_view(), name="rest"),
    path('rest-customer-login', views.rest_customer_login.as_view(), name="rest-customer-login"),
    path('Rest-Customer-Register', views.RestCustomerRegister.as_view(), name="Rest-Customer-Register"),
    path('rest-otp-login', views.rest_otp_login.as_view(), name="rest-otp-login"),
    path('rest-otp-verify', views.rest_otp_verify.as_view(), name="rest-otp-verify"),
    path('Rest-Customer-Homepage', views.RestCustomerHomepage.as_view(), name="Rest-Customer-Homepage"),
    path('Rest-Seeker-Carpenter-Detials', views.RestSeekerCarpenterDetials.as_view(), name="Rest-Seeker-Carpenter-Detials"),
    path('Rest-Seeker-Construction-Detials', views.RestSeekerConstructionDetials.as_view(), name="Rest-Seeker-Construction-Detials"),
    path('Rest-Seeker-Plumber-Detials', views.RestSeekerPlumberDetials.as_view(), name="Rest-Seeker-Plumber-Detials"),
    path('Rest-Seeker-Painter-Detials', views.RestSeekerPainterDetials.as_view(), name="Rest-Seeker-Painter-Detials"),
    path('Rest-Seeker-Catering-Detials', views.RestSeekerCateringDetials.as_view(), name="Rest-Seeker-Catering-Detials"),
    path('Rest-Seeker-Maid-Detials', views.RestSeekerMaidDetials.as_view(), name="Rest-Seeker-Maid-Detials"),
    path('Rest-Seeker-Electrician-Detials', views.RestSeekerMaidDetials.as_view(), name="Rest-Seeker-Maid-Detials"),
    path('Rest-Seeker-Welder-Detials', views.RestSeekerWelderDetials.as_view(), name="Rest-Seeker-Welder-Detials"),
    path('Rest-Seeker-Driver-Detials', views.RestSeekerDriverDetials.as_view(), name="Rest-Seeker-Driver-Detials"),












    path('seeker-profile', views.seeker_profile, name="seeker-profile"),
    path('seeker-logout', views.seeker_logout, name="seeker-logout"),
    path('seeker-available/<int:id>', views.seeker_available, name="seeker-available"),
    path('seeker-not-available/<int:id>', views.seeker_not_available, name="seeker-not-available"),
    path('edit-profile/<int:id>', views.edit_profile, name="edit-profile"),
    path('editing-profile', views.editing_profile, name="editing-profile"),
    path('seeker-order/<int:id>', views.seeker_order, name="seeker-order"),
    path('seeker-order-confirm/<int:id>', views.seeker_order_confirm, name="seeker-order-confirm"),
    path('seeker-feedback/<int:id>', views.seeker_feedback, name="seeker-feedback"),






    # path('test', views.test, name="test"),



    
]