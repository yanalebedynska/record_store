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
