from django.db import models

# COMPANY
class Company(models.Model):
    objects = None
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    contact_info = models.CharField(max_length=100, unique=True)
    web_site = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


    class Meta:
        db_table = 'company'