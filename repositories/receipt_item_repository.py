from ..models.receipt_item import ReceiptItem
from ..repositories.base_repository import BaseRepository
from django.db.models import Count, F


class ReceiptItemRepository(BaseRepository):
    def __init__(self):
        from ..models.receipt_item import ReceiptItem
        super().__init__(ReceiptItem)

    def get_products_with_order_count(self, min_orders):
        """
        Повертає список продуктів із кількістю замовлень, що більше або дорівнює min_orders.
        """
        return (
            self.model.objects.values('product__name')  # Збирає ім'я продукту
            .annotate(order_count=Count('product_id'))  # Підраховує кількість замовлень
            .filter(order_count__gte=min_orders)  # Фільтрує за кількістю замовлень
            .order_by('-order_count')  # Сортує за кількістю замовлень (за спаданням)
        )

    def get_orders_sorted_by_date(self):
        """
        Повертає замовлення, відсортовані від найновіших до найдавніших,
        із додаванням загальної ціни замовлення.
        """
        return self.model.objects.annotate(
            total_order_price=F('product__price') * F('quantity')
        ).order_by('-order_date')