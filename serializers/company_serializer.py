from rest_framework import serializers
from ..models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_id', 'name', 'contact_info', 'web_site']
