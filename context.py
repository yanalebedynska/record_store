from .repository import (
    EmployeeRoleRepository, EmployeeRepository, SupplierRepository,
    ConditionOfRecordRepository, RecordRepository, StoreUserRepository,
    ShippingAddressRepository, UserShippingAddressRepository,
    CreditCardRepository, OrderRepository, RecordInOrderRepository,
    TransactionInOrderRepository
)

# Базовий клас для контексту
class BaseContext:
    def __init__(self, repository):
        self.repo = repository

    def create(self, **kwargs):
        return self.repo.create(**kwargs)

    def add(self, **kwargs):
        return self.repo.create(**kwargs)

    def find_by_id(self, entity_id): 
        return self.repo.get_by_id(entity_id)


class Context:
    def __init__(self):
        # Ініціалізація всіх контекстів
        self.User = StoreUserContext()
        self.Employee = EmployeeContext()
        self.EmployeeRole = EmployeeRoleContext()
        self.Supplier = SupplierContext()
        self.ConditionOfRecord = ConditionOfRecordContext()
        self.Record = RecordContext()
        self.ShippingAddress = ShippingAddressContext()
        self.UserShippingAddress = UserShippingAddressContext()
        self.CreditCard = CreditCardContext()
        self.Order = OrderContext()
        self.RecordInOrder = RecordInOrderContext()
        self.TransactionInOrder = TransactionInOrderContext()

# Контекст користувача (StoreUser)
class StoreUserContext(BaseContext):
    def __init__(self):
        super().__init__(StoreUserRepository())


# Контекст співробітників (Employee)
class EmployeeContext(BaseContext):
    def __init__(self):
        super().__init__(EmployeeRepository())


# Контекст ролей співробітників (EmployeeRole)
class EmployeeRoleContext(BaseContext):
    def __init__(self):
        super().__init__(EmployeeRoleRepository())


# Контекст постачальників (Supplier)
class SupplierContext(BaseContext):
    def __init__(self):
        super().__init__(SupplierRepository())


# Контекст умов записів (ConditionOfRecord)
class ConditionOfRecordContext(BaseContext):
    def __init__(self):
        super().__init__(ConditionOfRecordRepository())


# Контекст записів (Record)
class RecordContext(BaseContext):
    def __init__(self):
        super().__init__(RecordRepository())


# Контекст адрес доставки (ShippingAddress)
class ShippingAddressContext(BaseContext):
    def __init__(self):
        super().__init__(ShippingAddressRepository())

# Контекст зв'язку користувача з адресою доставки (UserShippingAddress)
class UserShippingAddressContext(BaseContext):
    def __init__(self):
        super().__init__(UserShippingAddressRepository())


# Контекст кредитних карток (CreditCard)
class CreditCardContext(BaseContext):
    def __init__(self):
        super().__init__(CreditCardRepository())


# Контекст замовлень (Order)
class OrderContext(BaseContext):
    def __init__(self):
        super().__init__(OrderRepository())


# Контекст записів у замовленні (RecordInOrder)
class RecordInOrderContext(BaseContext):
    def __init__(self):
        super().__init__(RecordInOrderRepository())


# Контекст транзакцій у замовленні (TransactionInOrder)
class TransactionInOrderContext(BaseContext):
    def __init__(self):
        super().__init__(TransactionInOrderRepository())


# Створюємо глобальний об'єкт контексту, щоб використовувати в усьому додатку
context = Context()
