from ..models import Warehouse, Pharmacy
from rest_framework import serializers

class WarehouseSerializer(serializers.ModelSerializer):
    pharmacy = serializers.PrimaryKeyRelatedField(queryset=Pharmacy.objects.all(), allow_null=True)

    class Meta:
        model = Warehouse
        fields = ['warehouse_id', 'name', 'address', 'pharmacy']
