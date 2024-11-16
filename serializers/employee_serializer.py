from rest_framework import serializers
from ..models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'position', 'hire_date', 'salary', 'birthday_date']