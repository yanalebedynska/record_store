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


# RECORD
class Record(models.Model):
    record_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=False)
    artist = models.CharField(max_length=100, null=False)
    genre = models.CharField(max_length=50, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='records')
    condition = models.ForeignKey(ConditionOfRecord, on_delete=models.CASCADE, related_name='records')

    def str(self):
        return self.title


# STORE_USER
class StoreUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, null=False)
    user_password = models.CharField(max_length=150, null=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=False)
    email = models.EmailField(max_length=150, null=False)
    phonenumber = models.CharField(max_length=50, null=True, blank=True)

    def str(self):
        return self.username


# SHIPPING_ADDRESS
class ShippingAddress(models.Model):
    shipping_address_id = models.AutoField(primary_key=True)
    postal_code = models.IntegerField(null=False)
    country = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=150, null=False)
    city = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=50, null=False)

    def str(self):
        return f"{self.address}, {self.city}, {self.country}"


# USER SHIPPING ADDRESS
class UserShippingAddress(models.Model):
    user_shipping_address_id = models.AutoField(primary_key=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, related_name='user_addresses')
    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE, related_name='user_addresses')

# CREDIT CARD
class CreditCard(models.Model):
    card_id = models.AutoField(primary_key=True)
    expiring_date = models.DateField(null=False)
    arrears = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE, related_name='credit_cards')


# ORDER
class OrderInStore(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateField(null=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    tracking_number = models.IntegerField(null=False)
    quantity_of_records = models.IntegerField(null=False)
    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE, related_name='orders')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, related_name='orders')


# RECORD IN ORDER
class RecordInOrder(models.Model):
    record_in_table_id = models.AutoField(primary_key=True)
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='record_orders')
    order = models.ForeignKey(OrderInStore, on_delete=models.CASCADE, related_name='order_records')


# TRANSACTION IN ORDER
class TransactionInOrder(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    payment_date = models.DateField(null=False)
    payment_code = models.IntegerField(unique=True, null=False)
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey(OrderInStore, on_delete=models.CASCADE, related_name='transactions')
