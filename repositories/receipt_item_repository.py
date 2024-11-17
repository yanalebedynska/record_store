from ..models.receipt_item import ReceiptItem
from ..repositories.base_repository import BaseRepository


class ReceiptItemRepository(BaseRepository):
    def __init__(self):
        super().__init__(ReceiptItem)
