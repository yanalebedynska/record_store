from django.db import models

# EMPLOYEE_ROLE
class EmployeeRole(models.Model):
    employee_role_id = models.AutoField(primary_key=True)
    rolename = models.CharField(max_length=20, unique=True, null=False)

    def str(self):
        return self.rolename


# EMPLOYEE
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    emp_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    username = models.CharField(max_length=50, unique=True, null=False)
    phonenumber = models.CharField(max_length=25, null=False)
    age = models.IntegerField(null=False)
    emp_password = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    address = models.CharField(max_length=200, null=False)
    role = models.ForeignKey(EmployeeRole, on_delete=models.CASCADE, related_name='employees')

    def str(self):
        return f"{self.emp_name} {self.last_name}"

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(age__gte=18), name='check_employee_age'),
        ]


# SUPPLIER
class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supp_name = models.CharField(max_length=100, null=False)
    supp_info = models.TextField(null=False)
    address = models.CharField(max_length=100, default='is not mentioned')

    def str(self):
        return self.supp_name


# CONDITION OF RECORD
class ConditionOfRecord(models.Model):
    condition_id = models.AutoField(primary_key=True)
    condition_name = models.CharField(max_length=50, null=False)
    condition_description = models.TextField(null=False)

    def str(self):
        return self.condition_name
