from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name="admin-login"),
    path('admin-homepage', views.admin_homepage, name="admin-homepage"),
    path('admin-logout', views.admin_logout, name="admin-logout"),
    
    path('customer-management', views.customer_management, name="customer-management"), 
    path('add-customer', views.add_customer, name="add-customer"),
    path('delete-customer/<int:id>', views.delete_customer, name="delete-customer"),
    path('edit-customer/<int:id>', views.edit_customer, name="edit-customer"),
    path('save-edit/<int:id>', views.save_edit, name="save-edit"),

    path('seeker-manage', views.seeker_manage, name="seeker-manage"),
    path('add-seeker', views.add_seeker, name="add-seeker"),
    path('delete-seeker/<int:id>', views.delete_seeker, name="delete-seeker"),

    path('category-management', views.category_management, name="category-management"),
    path('add-category', views.add_category, name="add-category"),
    path('delete-category/<int:id>', views.delete_category, name="delete-category"),
    path('edit-category/<int:id>', views.edit_category, name="edit-category"),
    path('update-category/<int:id>', views.update_category, name="update-category"),
    path('edit-seeker/<int:id>', views.edit_seeker, name="edit-seeker"),
    path('feedback-admin', views.feedback_admin, name="feedback-admin"),
    path('report', views.report, name="report"),



    # path('rest-admin-login', views.rest_admin_login.as_view(), name="rest-admin-login"),

    


]