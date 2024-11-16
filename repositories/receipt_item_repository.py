from .base_repository import BaseRepository
from ..models.receipt_item import ReceiptItem

class ReceiptItemRepository(BaseRepository):
    def __init__(self):
        self._model = ReceiptItem

