from django.db import models
from .warehouse import Warehouse
from .product import Product

# WAREHOUSE_STOCK
class WarehouseStock(models.Model):
    objects = None
    warehouse_stock_id = models.AutoField(primary_key=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return f"{self.product.name} in {self.warehouse.name}"

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gte=0), name='check_stock_quantity_non_negative'),
            models.CheckConstraint(check=models.Q(price__gte=0), name='check_stock_price_non_negative')
        ]
        db_table = 'warehouse_stock'