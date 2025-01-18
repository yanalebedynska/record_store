from ..models.customer import Customer
from ..repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository):
    def __init__(self):
        super().__init__(Customer)

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def delete_by_id(self, pk):
        self.model.objects.filter(pk=pk).delete()