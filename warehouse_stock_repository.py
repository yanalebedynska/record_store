from .base_repository import BaseRepository
from ..models.warehouse_stock import WarehouseStock

class WarehouseStockRepository(BaseRepository):
    def __init__(self):
        self._model = WarehouseStock


