from rest_framework import serializers
from ..models import Pharmacy, Employee, Company


class PharmacySerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), allow_null=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), allow_null=True)

    class Meta:
        model = Pharmacy
        fields = ['pharmacy_id', 'name', 'address', 'contact_info', 'employee', 'company']