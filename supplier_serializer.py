from rest_framework import serializers
from ..models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    total_products = serializers.IntegerField(read_only=True)

    class Meta:
        model = Supplier
        fields = ['supplier_id', 'name', 'email', 'address', 'total_products']