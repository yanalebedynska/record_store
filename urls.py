from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pharmacyApp.views import (
    EmployeeViewSet, CompanyViewSet, CustomerViewSet, OrderViewSet, PharmacyViewSet,
    ProductViewSet, ReceiptViewSet, ReceiptItemViewSet, SupplierViewSet, TransactionViewSet,
    WarehouseViewSet, WarehouseStockViewSet, ProductsWithOrdersView, PopularSupplierView
)

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'pharmacies', PharmacyViewSet, basename='pharmacy')
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')
router.register(r'warehousestocks', WarehouseStockViewSet, basename='warehousestock')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'receipts', ReceiptViewSet, basename='receipt')
router.register(r'receiptitems', ReceiptItemViewSet, basename='receiptitem')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'transactions', TransactionViewSet, basename='transaction')


urlpatterns = [
    path('', include(router.urls)),
    path('products/', ProductViewSet.as_view({'get': 'list'}), name='products'),
    path('products_with_orders/', ProductsWithOrdersView.as_view({'get': 'list'}), name='products_with_orders'),
    path('popular-supplier/', PopularSupplierView.as_view({'get': 'list'}), name='popular_supplier_api'),
]