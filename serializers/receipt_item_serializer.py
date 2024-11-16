from ..models import ReceiptItem, WarehouseStock, Receipt
from rest_framework import serializers

class ReceiptItemSerializer(serializers.ModelSerializer):
    warehouse_stock = serializers.PrimaryKeyRelatedField(queryset=WarehouseStock.objects.all(), allow_null=True)
    receipt_id = serializers.PrimaryKeyRelatedField(queryset=Receipt.objects.all(), allow_null=True)

    class Meta:
        model = ReceiptItem
        fields = ['receipt_item_id', 'warehouse_stock', 'receipt_id', 'quantity']