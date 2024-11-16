from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from rest_framework.generics import get_object_or_404

from .forms import ProductForm, CustomerForm
from .NetworkHelper import NetworkHelper
from django.http import JsonResponse
from pharmacyApp.models import Product
from datetime import date  # Імпортуємо datetime



def home(request):
    return render(request, 'PharmacyInterface/home.html')


def product_list(request):
    products = NetworkHelper.get_list('products')
    return render(request, 'PharmacyInterface/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'PharmacyInterface/product_detail.html', {'object': product})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Дані пройшли валідацію, передаємо їх до API
            data = form.cleaned_data
            response = NetworkHelper.create_item('products', data)
            if response:
                messages.success(request, 'Product successfully created.')
                return redirect('PharmacyInterface:product_list')
            else:
                messages.error(request, 'Failed to create product.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()

    # Отримуємо список постачальників для вибору
    suppliers = NetworkHelper.get_list('suppliers')
    if suppliers:
        # Перевіряємо, чи список не порожній, та встановлюємо значення для choices
        form.fields['supplier'].choices = [(s['supplier_id'], s['name']) for s in suppliers]

    return render(request, 'PharmacyInterface/product_form.html', {'form': form})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('PharmacyInterface:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'PharmacyInterface/product_form.html', {'form': form})
def delete_object(request, item_id):
    if request.method == 'POST':
        result = NetworkHelper.delete_item('products', item_id)
        if result:
            return redirect('PharmacyInterface:product_list')
    return JsonResponse({"error": "Invalid request method."}, status=405)


def get_object(request, item_id):
    obj = NetworkHelper.get_item('products', item_id)
    if obj:
        return render(request, 'PharmacyInterface/product_detail.html', {'object': obj})
    else:
        return render(request, 'PharmacyInterface/error.html', {'message': 'Object not found.'})


def submit_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))
        product = NetworkHelper.get_item('products', product_id)

        if not product or quantity > product['quantity_in_stock']:
            messages.error(request, "Not enough product in stock")
            return render(request, 'PharmacyInterface/receipt_item.html')

        order_data = {'product_id': product_id, 'quantity': quantity, 'order_date': str(timezone.now())}
        NetworkHelper.create_item('orders', order_data)

        product['quantity_in_stock'] -= quantity
        NetworkHelper.update_item('products', product_id, product)
        messages.success(request, 'Order successfully added to order list.')
        return redirect('PharmacyInterface:receipt_item')
    return redirect('PharmacyInterface:home')


def order_list(request):
    """Список замовлень через API."""
    orders = NetworkHelper.get_list('orders')  # Отримуємо список замовлень через API
    if orders is None:
        orders = []  # Якщо API повернув None, замінюємо на порожній список
    total_orders = len(orders)  # Розрахунок кількості замовлень
    return render(request, 'PharmacyInterface/order_list.html', {'orders': orders, 'total_orders': total_orders})

def delete_order(request, order_id):
    result = NetworkHelper.delete_item('orders', order_id)
    if result:
        messages.success(request, 'Order successfully deleted.')
    return redirect('PharmacyInterface:order_list')


def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            NetworkHelper.create_item('customers', data)
            return redirect('PharmacyInterface:home')
    else:
        form = CustomerForm()
    return render(request, 'PharmacyInterface/customer_form.html', {'form': form})


def customer_list(request):
    customers = NetworkHelper.get_list('customers')
    return render(request, 'PharmacyInterface/customer_list.html', {'customers': customers})


def delete_customer(request, customer_id):
    result = NetworkHelper.delete_item('customers', customer_id)
    if result:
        messages.success(request, 'Customer successfully deleted.')
    return redirect('PharmacyInterface:customer_list')

def object_list(request):
    objects = NetworkHelper.get_list('objects')  # Припустимо, що є відповідний endpoint
    return render(request, 'PharmacyInterface/object_list.html', {'objects': objects})

def receipt_item(request):
    products = NetworkHelper.get_list('products')  # Припустимо, що ваш API має endpoint для отримання продуктів
    return render(request, 'PharmacyInterface/receipt_item.html', {'products': products})