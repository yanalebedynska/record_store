from django.db import models
from .order import Order

# RECEIPT
class Receipt(models.Model):
    objects = None
    receipt_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    data = models.DateField(null=False)
    amount_in_receipt = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    payment_method = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f"Receipt {self.receipt_id} for Order {self.order_id}"


    class Meta:
        db_table = 'receipt'