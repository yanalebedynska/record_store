from datetime import timedelta
from ..models import ReceiptItem
from django.utils import timezone

from ..repositories.base_repository import BaseRepository
from django.db.models import Count, F


class ReceiptItemRepository(BaseRepository):
    def __init__(self):
        from ..models.receipt_item import ReceiptItem
        super().__init__(ReceiptItem)

    #---
    def create(self, **validated_data):
        validated_data['warehouse_stock'] = validated_data.get('warehouse_stock', None)
        validated_data['receipt_id'] = validated_data.get('receipt_id', None)
        return self.model.objects.create(**validated_data)
    #--

    def delete_by_id(self, pk):
        self.model.objects.filter(pk=pk).delete()


    def get_products_with_order_count(self, min_orders):
        return (
            ReceiptItem.objects
            .values(product_name=F('product__name'))  # Отримуємо назву продукту
            .annotate(order_count=Count('receipt_item_id'))  # Підраховуємо кількість замовлень
            .filter(order_count__gte=min_orders)  # Фільтруємо за мінімальною кількістю
            .order_by('-order_count')  # Сортуємо у спадному порядку
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
