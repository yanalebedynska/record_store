from django.db import models
from .pharmacy import Pharmacy

# WAREHOUSE
class Warehouse(models.Model):
    objects = None
    warehouse_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=False)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


    class Meta:
        db_table = 'warehouse'