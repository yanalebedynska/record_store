from .base_repository import BaseRepository
from ..models.receipt import Receipt

class ReceiptRepository(BaseRepository):
    def __init__(self):
        self._model = Receipt


