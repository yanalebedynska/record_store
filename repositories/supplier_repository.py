from ..models.supplier import Supplier
from ..repositories.base_repository import BaseRepository


class SupplierRepository(BaseRepository):
    def __init__(self):
        super().__init__(Supplier)
