from ..models.product import Product
from ..repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__(Product)
