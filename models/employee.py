from django.db import models

# EMPLOYEE
class Employee(models.Model):
    objects = None
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    position = models.CharField(max_length=255, null=False)
    hire_date = models.DateField(null=False)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    birthday_date = models.DateField(null=False)

    def __str__(self):
        return f"{self.name} - {self.position}"

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(salary__gte=0), name='check_salary_non_negative')
        ]
        db_table = 'employee'