from django.db import models
from .supplier import Supplier

# PRODUCT
class Product(models.Model):
    objects = None
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity_in_stock = models.IntegerField(null=False)
    expiration_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(quantity_in_stock__gte=0), name='check_quantity_non_negative')
        ]
        db_table = 'product'