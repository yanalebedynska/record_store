from django.shortcuts import render
from django.utils import timezone

from pharmacyApp.repositories.product_repository import ProductRepository
from pharmacyApp.repositories.customer_repository import CustomerRepository
from pharmacyApp.repositories.receipt_item_repository import ReceiptItemRepository

from django.shortcuts import redirect
from .forms import ProductForm , CustomerForm
from django.http import JsonResponse
from django.contrib import messages

def home(request):
    return render(request, 'PharmacyInterface/home.html')

def product_list(request):
    products = ProductRepository().get_all()
    return render(request, 'PharmacyInterface/product_list.html', {'products': products})


def product_detail(request, pk):
    product = ProductRepository().get_by_id(pk)
    return render(request, 'PharmacyInterface/product_detail.html', {'object': product})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data.get('quantity_in_stock') is None:
                data['quantity_in_stock'] = 0
            ProductRepository().create(data)
            return redirect('PharmacyInterface:product_list')
    else:
        form = ProductForm()
    return render(request, 'PharmacyInterface/product_form.html', {'form': form})


def product_update(request, pk):
    product = ProductRepository().get_by_id(pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            ProductRepository.update(product, form.cleaned_data)
            return redirect('PharmacyInterface:product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'PharmacyInterface/product_form.html', {'form': form})



def receipt_item(request):
    products = ProductRepository().get_all()
    return render(request, 'PharmacyInterface/receipt_item.html', {'products': products})

def submit_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))
        product = ProductRepository().get_by_id(product_id)

        if quantity > product.quantity_in_stock:
            messages.error(request, "Not enough product in stock")
            return render(request, 'PharmacyInterface/receipt_item.html', {'products': ProductRepository().get_all()})

        ReceiptItemRepository().create({'product': product, 'quantity': quantity, 'order_date': timezone.now()})

        product_data = {'quantity_in_stock': product.quantity_in_stock - quantity}
        ProductRepository.update(product, product_data)

        messages.success(request, 'Order successfully added to order list.')
        return redirect('PharmacyInterface:receipt_item')

    return redirect('PharmacyInterface:home')

def order_list(request):
    orders = ReceiptItemRepository().get_all()
    total_orders = orders.count()
    return render(request, 'PharmacyInterface/order_list.html', {'orders': orders, 'total_orders': total_orders})


def delete_order(request, order_id):
    order = ReceiptItemRepository().get_by_id(order_id)
    ReceiptItemRepository.delete(order)
    messages.success(request, 'Order successfully deleted.')
    return redirect('PharmacyInterface:order_list')

def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            CustomerRepository().create(form.cleaned_data)
            return redirect('PharmacyInterface:home')
    else:
        form = CustomerForm()
    return render(request, 'PharmacyInterface/customer_form.html', {'form': form})


def customer_list(request):
    customers = CustomerRepository().get_all()
    return render(request, 'PharmacyInterface/customer_list.html', {'customers': customers})

def delete_customer(request, customer_id):
    customer = CustomerRepository().get_by_id(customer_id)
    CustomerRepository.delete(customer)
    messages.success(request, 'Customer successfully deleted.')
    return redirect('PharmacyInterface:customer_list')


def object_list(request):
    """
    Отримує список об'єктів через ProductRepository.
    """
    products = ProductRepository().get_all()  # Отримуємо всі продукти через репозиторій
    return render(request, 'object_list.html', {'objects': products})


def delete_object(request, item_id):
    """
    Видаляє об'єкт через ProductRepository.
    """
    if request.method == 'POST':
        try:
            product = ProductRepository().get_by_id(item_id)  # Отримуємо продукт через репозиторій
            if product:
                ProductRepository.delete(product)  # Видаляємо продукт через репозиторій
                messages.success(request, "Product successfully deleted.")
                return redirect('PharmacyInterface:product_list')
            else:
                messages.error(request, "Product not found.")
                return JsonResponse({"error": "Product not found."}, status=404)
        except Exception as e:
            print("Delete object error:", e)
            return JsonResponse({"error": "Delete object error."}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=405)


def get_object(request, item_id):
    """
    Отримує конкретний об'єкт через ProductRepository.
    """
    product = ProductRepository().get_by_id(item_id)  # Отримуємо продукт через репозиторій
    if product:
        return render(request, 'product_detail.html', {'object': product})
    else:
        return render(request, 'error.html', {'message': 'Object not found.'})