from ..models import Transaction, Receipt
from rest_framework import serializers

class TransactionSerializer(serializers.ModelSerializer):
    receipt = serializers.PrimaryKeyRelatedField(queryset=Receipt.objects.all(), allow_null=True)

    class Meta:
        model = Transaction
        fields = ['transaction_id', 'receipt', 'date', 'amount', 'type_of_transaction', 'status']