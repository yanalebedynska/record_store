from ..models.customer import Customer
from ..repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository):
    def __init__(self):
        super().__init__(Customer)
