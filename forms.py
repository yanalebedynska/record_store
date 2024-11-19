from django import forms
from pharmacyApp.models import Product, ReceiptItem, Customer

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'expiration_date', 'category', 'supplier', 'quantity_in_stock']


class ReceiptItemForm(forms.ModelForm):
    class Meta:
        model = ReceiptItem
        fields = ['warehouse_stock', 'quantity']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_number']