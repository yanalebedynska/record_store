from ..models import Product, Supplier
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), allow_null=True)

    class Meta:
        model = Product
        fields = ['product_id', 'name', 'supplier', 'quantity_in_stock', 'expiration_date', 'category']