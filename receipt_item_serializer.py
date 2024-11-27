from ..models import ReceiptItem, WarehouseStock, Receipt, Product
from rest_framework import serializers

class ReceiptItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    total_order_price = serializers.SerializerMethodField()
    #--
    warehouse_stock = serializers.PrimaryKeyRelatedField(queryset=WarehouseStock.objects.all(), allow_null=True, required=False, default=None)
    receipt_id = serializers.PrimaryKeyRelatedField(queryset=Receipt.objects.all(), allow_null=True, required=False, default=None)
    #--

    class Meta:
        model = ReceiptItem
        fields = ['receipt_item_id', 'product_name', 'product_price', 'quantity', 'total_order_price',
                  'warehouse_stock', 'receipt_id', 'product']#--

    '''def get_total_order_price(self, obj):
        return obj.quantity * obj.product.price if obj.product and obj.product.price else 0'''

    #--
    def get_total_order_price(self, obj):
        if isinstance(obj, dict):  # Якщо obj — це словник
            product_id = obj.get('product')
            quantity = obj.get('quantity', 1)
            if product_id:
                product = Product.objects.filter(id=product_id).first()
                if product and product.price:
                    return quantity * product.price
            return 0
        else:  # Якщо obj — це інстанція моделі
            return obj.quantity * obj.product.price if obj.product and obj.product.price else 0