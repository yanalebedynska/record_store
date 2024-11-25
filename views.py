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
        data = list(queryset)  # Перетворюємо queryset у список
        df = pd.DataFrame(data)  # Перетворюємо у DataFrame

        # Формування даних для відповіді
        return {
            "chart_data": df.to_dict(orient='records')  # Дані для графіка
        }

    @action(detail=False, methods=['get'], url_path='receiptitems-stats')
    def receiptitems_stats(self, request, *args, **kwargs):
        """
        Custom endpoint to retrieve statistical analysis for receipt items' data.
        """
        queryset = self.get_repository().get_all()  # Отримуємо всі дані через репозиторій
        data = list(queryset.values('receipt_item_id', 'quantity', 'product__price'))  # Обираємо потрібні поля

        # Перевірка, чи є дані
        if not data:
            return Response({
                "chart_data": [],  # Повертаємо порожній список, якщо даних немає
                "message": "No data available for statistical analysis."
            })

        # Перетворюємо дані у pandas DataFrame
        df = pd.DataFrame(data)

        # Перевіряємо, чи є необхідні стовпці
        if 'quantity' not in df.columns or 'product__price' not in df.columns:
            return Response({
                "chart_data": [],
                "message": "Required columns are missing."
            })

        # Групування для графіка
        df_grouped = df.groupby('receipt_item_id', as_index=False).sum()

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

        # Формування даних для відповіді
        return {
            "chart_data": df_grouped.to_dict(orient='records'),
            "stats": stats
        }

    @action(detail=False, methods=['get'], url_path='receiptitems-grouped-stats')
    def receiptitems_grouped_stats(self, request, *args, **kwargs):
        """
        Custom endpoint to group and aggregate receipt items data.
        Aggregates data by product categories and days.
        """
        queryset = self.get_repository().get_all()
        data = queryset.values('product__category', 'order_date', 'quantity', 'product__price')
        df = pd.DataFrame(list(data))

        # Перевірка, чи є дані
        if df.empty:
            return {
                "by_category": [],
                "by_day": [],
                "message": "No data available for grouped analysis."
            }

        # Перетворення `order_date` у формат дати
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df = df.dropna(subset=['order_date'])  # Видаляємо рядки з некоректною датою

        # Додавання нового стовпця з загальною вартістю
        df['total_income'] = df['quantity'] * df['product__price']

        # Групування по днях
        day_group = df.groupby(df['order_date'].dt.strftime('%Y-%m-%d')).agg(
            total_income=('total_income', 'sum'),
            total_quantity=('quantity', 'sum')
        ).reset_index()

        # Перейменовуємо колонку групування на "day"
        day_group.rename(columns={"order_date": "day"}, inplace=True)

        # Формування результату
        return {
            "by_day": day_group.to_dict(orient='records')
        }


class SupplierViewSet(BaseViewSet):
    serializer_class = SupplierSerializer

    def get_repository(self):
        return SupplierRepository()

    @action(detail=False, methods=['get'], url_path='suppliers-with-product-count')
    def suppliers_with_product_count(self, request, *args, **kwargs):
        # Отримуємо дані через репозиторій
        queryset = self.get_repository().get_suppliers_with_product_count()

        # Приведення queryset до списку словників
        data = list(queryset.values('name', 'total_products'))

        # Перевірка, чи є дані
        if not data:
            return {
                "chart_data": []
            }

        # Повертаємо дані
        return {
            "chart_data": data  # Дані у вигляді списку словників
        }

    @action(detail=False, methods=['get'], url_path='suppliers-stats')
    def suppliers_stats(self, request, *args, **kwargs):
        """
        Custom endpoint to retrieve statistical analysis for suppliers' data.
        """
        queryset = self.get_repository().get_suppliers_with_product_count()
        data = list(queryset.values('supplier_id', 'name', 'total_products'))

        # Перевірка, чи є дані
        if not data:
            return {
                "chart_data": [],
                "message": "No data available for statistical analysis."
            }

        # Перетворення в pandas DataFrame
        df = pd.DataFrame(data)

        # Перевірка колонок
        if 'total_products' not in df.columns:
            return {
                "chart_data": [],
                "message": "Required columns are missing."
            }

        # Групування для графіка
        df_grouped = df.groupby('supplier_id', as_index=False).sum()

        # Обчислення статистики
        stats = {
            "total_products": {
                "mean": df['total_products'].mean(),
                "median": df['total_products'].median(),
                "min": df['total_products'].min(),
                "max": df['total_products'].max()
            }
        }

        # Формування даних для відповіді
        return {
            "chart_data": df_grouped.to_dict(orient='records'),
            "stats": stats
        }

    @action(detail=False, methods=['get'], url_path='suppliers-grouped-stats')
    def suppliers_grouped_stats(self, request, *args, **kwargs):
        """
        Custom endpoint to group and aggregate suppliers' data.
        Aggregates data by total products.
        """
        queryset = self.get_repository().get_suppliers_with_product_count()
        data = list(queryset.values('supplier_id', 'name', 'total_products'))

        # Перевірка, чи є дані
        if not data:
            return {
                "by_total_products": [],
                "message": "No data available for grouped analysis."
            }

        # Групування по кількості продуктів
        product_group = {}
        for item in data:
            total_products = item["total_products"]
            if total_products not in product_group:
                product_group[total_products] = {"total_suppliers": 0, "total_products": total_products}
            product_group[total_products]["total_suppliers"] += 1

        # Перетворення у список
        grouped_data = list(product_group.values())
        grouped_data = sorted(grouped_data, key=lambda x: x["total_products"])

        # Формування результату
        return {
            "by_total_products": grouped_data
        }
