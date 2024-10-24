from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Employee, EmployeeRole, Supplier, ConditionOfRecord, Record,
    StoreUser, ShippingAddress, UserShippingAddress, CreditCard,
    OrderInStore, RecordInOrder, TransactionInOrder
)

# Базовий клас для репозиторіїв з інкапсуляцією
class BaseRepository:
    _model = None  # захищений атрибут для моделі

    def get_all(self):
        """Отримати всі записи моделі"""
        return self._model.objects.all()

    def get_by_id(self, pk):
        """Отримати запис по ID (захищений метод)"""
        return self._get_by_id(pk)

    def create(self, **kwargs):
        """Створити новий запис"""
        return self._model.objects.create(**kwargs)

    def _get_by_id(self, pk):
        """Захищений метод для пошуку по ID"""
        try:
            return self._model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None


# Репозиторій для EmployeeRole
class EmployeeRoleRepository(BaseRepository):
    def __init__(self):
        self._model = EmployeeRole  # Призначаємо модель через інкапсуляцію


# Репозиторій для Employee
class EmployeeRepository(BaseRepository):
    def __init__(self):
        self._model = Employee  # Призначаємо модель через інкапсуляцію

class SupplierRepository(BaseRepository):
    def __init__(self):
        self._model = Supplier

class ConditionOfRecordRepository(BaseRepository):
    def __init__(self):
        self._model = ConditionOfRecord

class RecordRepository(BaseRepository):
    def __init__(self):
        self._model = Record

class StoreUserRepository(BaseRepository):
    def __init__(self):
        self._model = StoreUser

class ShippingAddressRepository(BaseRepository):
    def __init__(self):
        self._model = ShippingAddress

class UserShippingAddressRepository(BaseRepository):
    def __init__(self):
        self._model = UserShippingAddress

class CreditCardRepository(BaseRepository):
    def __init__(self):
        self._model = CreditCard

class OrderRepository(BaseRepository):
    def __init__(self):
        self._model = OrderInStore

class RecordInOrderRepository(BaseRepository):
    def __init__(self):
        self._model = RecordInOrder

class TransactionInOrderRepository(BaseRepository):
    def __init__(self):
        self._model = TransactionInOrder
