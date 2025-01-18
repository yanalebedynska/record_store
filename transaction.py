from django.db import models
from .receipt import Receipt

# TRANSACTION
class Transaction(models.Model):
    objects = None
    transaction_id = models.AutoField(primary_key=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    type_of_transaction = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=55, null=False)

    def __str__(self):
        return f"Transaction {self.transaction_id}"

    class Meta:
        db_table = 'transactions'