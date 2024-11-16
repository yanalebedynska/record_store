from .base_repository import BaseRepository
from ..models.supplier import Supplier

class SupplierRepository(BaseRepository):
    def __init__(self):
        self._model = Supplier
