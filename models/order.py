from django.db import models
from .customer import Customer
from .warehouse_stock import WarehouseStock, Product

# ORDER
class Order(models.Model):
    objects = None
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateField(null=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    warehouse_stock = models.ForeignKey(WarehouseStock, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.customer.name}"

    class Meta:
        db_table = 'order'