from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

from rest_framework.response import Response
from rest_framework.decorators import action

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


class ReceiptItemViewSet(BaseViewSet):
    serializer_class = ReceiptItemSerializer

    def get_repository(self):
        return ReceiptItemRepository()


class SupplierViewSet(BaseViewSet):
    serializer_class = SupplierSerializer

    def get_repository(self):
        return SupplierRepository()


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