from django.contrib import admin
from pharmacyApp.models import Product, Customer, Company, Employee, Order, Pharmacy, Receipt, ReceiptItem, Supplier, Transaction, Warehouse, WarehouseStock

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Order)
admin.site.register(Pharmacy)
admin.site.register(Receipt)
admin.site.register(ReceiptItem)
admin.site.register(Supplier)
admin.site.register(Transaction)
admin.site.register(Warehouse)
admin.site.register(WarehouseStock)