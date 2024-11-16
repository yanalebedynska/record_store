from .base_repository import BaseRepository
from ..models.company import Company

class CompanyRepository(BaseRepository):
    def __init__(self):
        self._model = Company

