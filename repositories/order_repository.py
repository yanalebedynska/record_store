from .base_repository import BaseRepository
from ..models.order import Order

class OrderRepository(BaseRepository):
    def __init__(self):
        self._model = Order

    def read_all(self):
        return self._model.objects.select_related('customer', 'warehouse_stock').all()