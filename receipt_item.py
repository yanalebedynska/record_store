from django.db import models
from django.utils import timezone

from .warehouse_stock import WarehouseStock
from .product import Product


# RECEIPT_ITEM
class ReceiptItem(models.Model):
    objects = None
    receipt_item_id = models.AutoField(primary_key=True)
    warehouse_stock = models.ForeignKey(
        WarehouseStock, on_delete=models.CASCADE, null=True, blank=True  # Робимо поле необов'язковим
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateTimeField(default=timezone.now)
    receipt_id = models.ForeignKey('Receipt', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return f"Item {self.receipt_item_id} for Receipt {self.receipt_id}"

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gt=0), name='check_quantity_positive')
        ]
        db_table = 'receipt_item'