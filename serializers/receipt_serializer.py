from ..models import Receipt, Order
from rest_framework import serializers

class ReceiptSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), allow_null=True)

    class Meta:
        model = Receipt
        fields = ['receipt_id', 'order_id', 'data', 'amount_in_receipt', 'payment_method']