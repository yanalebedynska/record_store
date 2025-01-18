from ..models import WarehouseStock, Warehouse, Product
from rest_framework import serializers

class WarehouseStockSerializer(serializers.ModelSerializer):
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all(), allow_null=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), allow_null=True)

    class Meta:
        model = WarehouseStock
        fields = ['warehouse_stock_id', 'warehouse', 'product', 'quantity', 'price']
