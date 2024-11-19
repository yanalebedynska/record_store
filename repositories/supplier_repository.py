from ..models.supplier import Supplier
from ..repositories.base_repository import BaseRepository
from django.db.models import Count

class SupplierRepository(BaseRepository):
    def __init__(self):
        super().__init__(Supplier)

    def get_suppliers_with_product_count(self):
        """
        Отримує постачальників із підрахунком кількості продуктів.
        """
        return self.model.objects.annotate(total_products=Count('product')).order_by('-total_products')