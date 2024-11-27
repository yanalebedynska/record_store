from django.db import models

# SUPPLIER
class Supplier(models.Model):
    objects = None
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50, unique=True)
    address = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


    class Meta:
        db_table = 'supplier'