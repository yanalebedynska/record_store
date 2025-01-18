from .base_repository import BaseRepository
from ..models.order import Order

class OrderRepository(BaseRepository):
    def __init__(self):
        super().__init__(Order)

    def read_all(self):
        return self.model.objects.select_related('customer', 'warehouse_stock').all()