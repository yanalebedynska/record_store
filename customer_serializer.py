from rest_framework import serializers
from ..models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer  # Вказуємо модель
        fields = ['customer_id', 'name', 'email', 'phone_number', 'address']  # Вказуємо конкретні поля