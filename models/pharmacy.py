from django.db import models
from .employee import Employee
from .company import Company

# PHARMACY
class Pharmacy(models.Model):
    objects = None
    pharmacy_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=50, null=False)
    contact_info = models.CharField(max_length=250, unique=True, null=False)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


    class Meta:
        db_table = 'pharmacy'