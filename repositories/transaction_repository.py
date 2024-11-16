from .base_repository import BaseRepository
from ..models.transaction import Transaction

class TransactionRepository(BaseRepository):
    def __init__(self):
        self._model = Transaction

    def read_all(self):
        pass