from .base_repository import BaseRepository
from ..models.pharmacy import Pharmacy

class PharmacyRepository(BaseRepository):
    def __init__(self):
        self._model = Pharmacy

    def read_all(self):
        pass