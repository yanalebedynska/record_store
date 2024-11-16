from .company_repository import CompanyRepository
from .customer_repository import CustomerRepository
from .employee_repository import EmployeeRepository
from .order_repository import OrderRepository
from .pharmacy_repository import PharmacyRepository
from .product_repository import ProductRepository
from .receipt_item_repository import ReceiptItemRepository
from .receipt_repository import ReceiptRepository
from .supplier_repository import SupplierRepository
from .transaction_repository import TransactionRepository
from .warehouse_repository import WarehouseRepository
from .warehouse_stock_repository import WarehouseStockRepository
'''from ..repositories import (
    company_repository, customer_repository, employee_repository, order_repository, pharmacy_repository,
    product_repository, receipt_item_repository, receipt_repository, supplier_repository, transaction_repository,
    warehouse_repository, warehouse_stock_repository
)
'''

class Context:
    def __init__(self):
        self.Companies = CompanyRepository()
        self.Customers = CustomerRepository()
        self.Employees = EmployeeRepository()
        self.Orders = OrderRepository()
        self.Pharmacies = PharmacyRepository()
        self.Products = ProductRepository()
        self.Receipts = ReceiptRepository()
        self.Suppliers = SupplierRepository()
        self.Warehouses = WarehouseRepository()
        self.WarehouseStocks = WarehouseStockRepository()
        self.Transactions = TransactionRepository()
        self.ReceiptItems = ReceiptItemRepository()