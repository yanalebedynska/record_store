from django.db.models import Avg
from .base_repository import BaseRepository
from ..models.employee import Employee

class EmployeeRepository(BaseRepository):
    def __init__(self):
        self._model = Employee

    def get_average_salary(self):
        return self._model.objects.aggregate(Avg('salary'))['salary__avg']