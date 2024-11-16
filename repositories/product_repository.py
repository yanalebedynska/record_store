from .base_repository import BaseRepository
from ..models.product import Product

class ProductRepository(BaseRepository):
    def __init__(self):
        self._model = Product

