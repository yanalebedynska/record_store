from django import forms
from pharmacyApp.models import Product, ReceiptItem, Customer

class ProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    expiration_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    category = forms.CharField(max_length=100)
    supplier = forms.IntegerField(widget=forms.Select())  # ID постачальника
    quantity_in_stock = forms.IntegerField(min_value=0)

class ReceiptItemForm(forms.ModelForm):
    class Meta:
        model = ReceiptItem
        fields = ['warehouse_stock', 'quantity']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_number']
