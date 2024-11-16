from django.urls import path
from . import views
from .views import product_detail

app_name = 'PharmacyInterface'

urlpatterns = [
    path('', views.home, name='home'),  # Маршрут для домашньої сторінки
    path('products/', views.product_list, name='product_list'),
    path('product/delete/<int:item_id>/', views.delete_object, name='delete_object'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('add/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('objects/', views.object_list, name='object_list'),
    path('objects/<int:item_id>/', views.get_object, name='get_object'),

    path('receipt_item/', views.receipt_item, name='receipt_item'),

    path('submit_order/', views.submit_order, name='submit_order'),
    path('order_list/', views.order_list, name='order_list'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),

    path('add_customer/', views.add_customer, name='customer_create'),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('delete_customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),
]