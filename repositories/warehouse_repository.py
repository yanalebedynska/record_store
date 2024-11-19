from .base_repository import BaseRepository
from ..models.warehouse import Warehouse

class WarehouseRepository(BaseRepository):
    def __init__(self):
        self._model = Warehouse

    def read_all(self):
        pass