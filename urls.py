from django.urls import path
from . import views
from .views import product_detail
from .views import popular_supplier_view

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

    path('popular-supplier/', popular_supplier_view, name='popular_supplier'),
    path('products_with_orders/', views.products_with_orders_view, name='products_with_orders'),

    path('dashboardPlotly/', views.dashboardPlotly, name='dashboardPlotly'),
    path('dashboardPlotly/plotly-bar/', views.plotly_bar_chart_1, name='plotly_bar_chart_1'),
    path('dashboardPlotly/plotly-pie/', views.plotly_pie_chart_2, name='plotly_pie_chart_2'),
    path('dashboardPlotly/plotly-bar-2', views.plotly_bar_chart_3, name='plotly_bar_chart_3'),
    path('dashboardPlotly/plotly-line/', views.plotly_line_chart_4, name='plotly_line_chart_4'),
    path('dashboardPlotly/plotly-pie-2/', views.plotly_pie_chart_5, name='plotly_pie_chart_5'),
    path('dashboardPlotly/plotly-area/', views.plotly_area_chart_6, name='plotly_area_chart_6'),

    path('dashboardBokeh/', views.dashboardBokeh, name='dashboardBokeh'),
    path('dashboardBokeh/bokeh-bar-1/', views.bokeh_bar_chart_1, name='bokeh_bar_chart_1'),
    path('dashboardBokeh/bokeh-pie-2/', views.bokeh_pie_chart_2, name='bokeh_pie_chart_2'),
    path('dashboardBokeh/bokeh-bar-3/', views.bokeh_bar_chart_3, name='bokeh_bar_chart_3'),
    path('dashboardBokeh/bokeh-line/', views.bokeh_line_chart_4, name='bokeh_line_chart_4'),
    path('dashboardBokeh/bokeh-pie-3/', views.bokeh_pie_chart_5, name='bokeh_pie_chart_5'),
    path('dashboardBokeh/bokeh-area/', views.bokeh_area_chart_6, name='bokeh_area_chart_6'),
]