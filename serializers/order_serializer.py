from ..models import Order, Customer, WarehouseStock
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), allow_null=True)
    warehouse_stock = serializers.PrimaryKeyRelatedField(queryset=WarehouseStock.objects.all(), allow_null=True)

    class Meta:
        model = Order
        fields = ['order_id', 'order_date', 'customer', 'warehouse_stock']