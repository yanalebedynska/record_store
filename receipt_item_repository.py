from datetime import timedelta

from django.utils import timezone

from ..repositories.base_repository import BaseRepository
from django.db.models import Count, F


class ReceiptItemRepository(BaseRepository):
    def __init__(self):
        from ..models.receipt_item import ReceiptItem
        super().__init__(ReceiptItem)

    def delete_by_id(self, pk):
        self.model.objects.filter(pk=pk).delete()

    def get_products_with_order_count(self, min_orders):
        return (
            self.model.objects.values('product__name')
            .annotate(order_count=Count('product_id'))
            .filter(order_count__gte=min_orders)
            .order_by('-order_count')
        )

    def get_orders_sorted_by_date(self):
        return self.model.objects.annotate(
            total_order_price=F('product__price') * F('quantity')
        ).order_by('-order_date')

    def get_filtered_items(self, category=None, min_value=0, date_range=0):
        queryset = self.get_all()

        if category and category != "all":
            queryset = queryset.filter(product__category=category)

        queryset = queryset.filter(quantity__gte=min_value)

        if date_range > 0:
            start_date = timezone.now() - timedelta(days=date_range)
            queryset = queryset.filter(order_date__gte=start_date)

        return queryset
