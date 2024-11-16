from .base_repository import BaseRepository
from ..models.customer import Customer

class CustomerRepository(BaseRepository):
    def __init__(self):
        self._model = Customer

    def read_all(self):
        pass