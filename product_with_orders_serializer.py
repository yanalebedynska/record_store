from rest_framework import serializers

class ProductWithOrdersSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    order_count = serializers.IntegerField()

