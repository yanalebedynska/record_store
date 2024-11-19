from rest_framework import viewsets  #Містить класи для створення наборів виглядів, які поєднують логіку перегляду та запитів.
#для спрощення процесу створення API, забезпечуючи готові методи для обробки запитів CRUD
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

from .serializers import (
EmployeeSerializer, OrderSerializer, CompanySerializer, CustomerSerializer, PharmacySerializer,
ProductSerializer, ReceiptSerializer, ReceiptItemSerializer, SupplierSerializer, TransactionSerializer,
WarehouseSerializer, WarehouseStockSerializer
)

from .repositories.company_repository import CompanyRepository
from .repositories.customer_repository import CustomerRepository
from .repositories.employee_repository import EmployeeRepository
from .repositories.order_repository import OrderRepository
from .repositories.pharmacy_repository import PharmacyRepository
from .repositories.product_repository import ProductRepository
from .repositories.receipt_item_repository import ReceiptItemRepository
from .repositories.receipt_repository import ReceiptRepository
from .repositories.supplier_repository import SupplierRepository
from .repositories.transaction_repository import TransactionRepository
from .repositories.warehouse_repository import WarehouseRepository
from .repositories.warehouse_stock_repository import WarehouseStockRepository

import pandas as pd
from rest_framework.decorators import action
from rest_framework.response import Response


class BaseViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        repository = self.get_repository()
        return repository.read_all()

    def perform_create(self, serializer):
        repository = self.get_repository()
        repository.create(**serializer.validated_data)

    def perform_update(self, serializer):
        repository = self.get_repository()
        repository.update(serializer.instance.pk, **serializer.validated_data)

    def perform_destroy(self, instance):
        repository = self.get_repository()
        repository.delete_by_id(instance.pk)

    def get_repository(self):
        raise NotImplementedError("You should implement this method.")



class EmployeeViewSet(BaseViewSet):
    serializer_class = EmployeeSerializer

    def get_repository(self):
        return EmployeeRepository()

    @action(detail=False, methods=['get'])
    def report_avg_salary(self, request, *args, **kwargs):
        average_salary = self.get_repository().get_average_salary()
        return Response({"average_salary": average_salary})


class OrderViewSet(BaseViewSet):
    serializer_class = OrderSerializer

    def get_repository(self):
        return OrderRepository()


class CompanyViewSet(BaseViewSet):
    serializer_class = CompanySerializer

    def get_repository(self):
        return CompanyRepository()


class CustomerViewSet(BaseViewSet):
    serializer_class = CustomerSerializer

    def get_repository(self):
        return CustomerRepository()


class PharmacyViewSet(BaseViewSet):
    serializer_class = PharmacySerializer

    def get_repository(self):
        return PharmacyRepository()


class ProductViewSet(BaseViewSet):
    serializer_class = ProductSerializer

    def get_repository(self):
        return ProductRepository()


class ReceiptViewSet(BaseViewSet):
    serializer_class = ReceiptSerializer

    def get_repository(self):
        return ReceiptRepository()

class TransactionViewSet(BaseViewSet):
    serializer_class = TransactionSerializer

    def get_repository(self):
        return TransactionRepository()

class WarehouseViewSet(BaseViewSet):
    serializer_class = WarehouseSerializer

    def get_repository(self):
        return WarehouseRepository()


class WarehouseStockViewSet(BaseViewSet):
    serializer_class = WarehouseStockSerializer

    def get_repository(self):
        return WarehouseStockRepository()

#------------------------------------------------------------------------------------------------------------
class ReceiptItemViewSet(BaseViewSet):
    serializer_class = ReceiptItemSerializer

    def get_repository(self):
        return ReceiptItemRepository()


    @action(detail=False, methods=['get'], url_path='products-with-order-count')
    def products_with_order_count(self, request, *args, **kwargs):
        min_orders = int(request.query_params.get('min_orders', 1))
        queryset = self.get_repository().get_products_with_order_count(min_orders)
        data = list(queryset)
        df = pd.DataFrame(data)
        return Response(df.to_dict(orient='records'))

    @action(detail=False, methods=['get'], url_path='receiptitems-stats')
    def receiptitems_stats(self, request, *args, **kwargs):
        """
        Custom endpoint to retrieve statistical analysis for receipt items' data.
        """
        queryset = self.get_repository().get_all()  # Отримуємо всі дані через репозиторій
        data = queryset.values('receipt_item_id', 'quantity', 'product__price')  # Обираємо потрібні поля
        df = pd.DataFrame(list(data))  # Перетворюємо дані у pandas DataFrame

        # Перевірка, чи є дані
        if df.empty:
            return Response({"message": "No data available for statistical analysis."})

        # Обчислення статистики
        stats = {
            "quantity": {
                "mean": df['quantity'].mean(),
                "median": df['quantity'].median(),
                "min": df['quantity'].min(),
                "max": df['quantity'].max()
            },
            "price": {
                "mean": df['product__price'].mean(),
                "median": df['product__price'].median(),
                "min": df['product__price'].min(),
                "max": df['product__price'].max()
            }
        }
        return Response(stats)

    @action(detail=False, methods=['get'], url_path='receiptitems-grouped-stats')
    def receiptitems_grouped_stats(self, request, *args, **kwargs):
        """
        Custom endpoint to group and aggregate receipt items data.
        Aggregates data by product categories and months.
        """
        queryset = self.get_repository().get_all()
        data = queryset.values('product__category', 'order_date', 'quantity', 'product__price')
        df = pd.DataFrame(list(data))

        # Перевірка, чи є дані
        if df.empty:
            return Response({"message": "No data available for grouped analysis."})

        # Перетворення дати в формат місяця
        df['month'] = pd.to_datetime(df['order_date']).dt.strftime('%Y-%m')

        # Додавання нового стовпця з загальною вартістю
        df['total_income'] = df['quantity'] * df['product__price']

        # Групування по категорії товару
        category_group = df.groupby('product__category').agg(
            total_income=('total_income', 'sum'),
            average_income=('total_income', 'mean'),
            total_quantity=('quantity', 'sum')
        ).reset_index()

        # Групування по місяцях
        month_group = df.groupby('month').agg(
            total_income=('total_income', 'sum'),
            average_income=('total_income', 'mean'),
            total_quantity=('quantity', 'sum')
        ).reset_index()

        # Формування результату
        result = {
            "by_category": category_group.to_dict(orient='records'),
            "by_month": month_group.to_dict(orient='records')
        }
        return Response(result)


class SupplierViewSet(BaseViewSet):
    serializer_class = SupplierSerializer

    def get_repository(self):
        return SupplierRepository()

    @action(detail=False, methods=['get'], url_path='suppliers-with-product-count')
    def suppliers_with_product_count(self, request, *args, **kwargs):
        queryset = self.get_repository().get_suppliers_with_product_count()
        data = queryset.values('supplier_id', 'name', 'total_products')
        df = pd.DataFrame(list(data))
        return Response(df.to_dict(orient='records'))

    @action(detail=False, methods=['get'], url_path='suppliers-stats')
    def suppliers_stats(self, request, *args, **kwargs):
        """
        Custom endpoint to retrieve statistical analysis for suppliers' data.
        """
        queryset = self.get_repository().get_suppliers_with_product_count()
        data = queryset.values('supplier_id', 'name', 'total_products')
        df = pd.DataFrame(list(data))  # Перетворення в pandas DataFrame

        # Перевірка, чи є дані
        if df.empty:
            return Response({"message": "No data available for statistical analysis."})

        # Обчислення статистики
        stats = {
            "total_products": {
                "mean": df['total_products'].mean(),
                "median": df['total_products'].median(),
                "min": df['total_products'].min(),
                "max": df['total_products'].max()
            }
        }
        return Response(stats)

    @action(detail=False, methods=['get'], url_path='suppliers-grouped-stats')
    def suppliers_grouped_stats(self, request, *args, **kwargs):
        """
        Custom endpoint to group and aggregate suppliers' data.
        Aggregates data by total products.
        """
        queryset = self.get_repository().get_suppliers_with_product_count()
        data = queryset.values('supplier_id', 'name', 'total_products')
        df = pd.DataFrame(list(data))

        # Перевірка, чи є дані
        if df.empty:
            return Response({"message": "No data available for grouped analysis."})

        # Групування по кількості продуктів
        product_group = df.groupby('total_products').agg(
            total_suppliers=('supplier_id', 'count'),
            average_products=('total_products', 'mean')
        ).reset_index()

        product_group = product_group.sort_values(by='total_suppliers', ascending=False)

        # Формування результату
        result = {
            "by_total_products": product_group.to_dict(orient='records')
        }
        return Response(result)