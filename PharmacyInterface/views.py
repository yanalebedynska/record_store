from django.shortcuts import render
from django.utils import timezone

from pharmacyApp.models import Product, ReceiptItem, Order, Customer

from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .forms import ProductForm , CustomerForm
from .NetworkHelper import NetworkHelper
from django.http import JsonResponse
from django.contrib import messages

def home(request):
    return render(request, 'PharmacyInterface/home.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'PharmacyInterface/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'PharmacyInterface/product_detail.html', {'object': product})


#---------------------------------------------------------------------------------------------------------------------------------------
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            if product.quantity_in_stock is None:
                product.quantity_in_stock = 0
            product.save()
            return redirect('PharmacyInterface:product_list')
    else:
        form = ProductForm()
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
#------------------------------------------------------------------------------------------------------------------------------------------

def object_list(request):
    objects = NetworkHelper.get_list()  # отримуємо список об'єктів з API
    return render(request, 'object_list.html', {'objects': objects})


def delete_object(request, item_id):
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, pk=item_id)
            product.delete()
            return redirect('PharmacyInterface:product_list')
        except Exception as e:
            print("Delete object error:", e)
            return JsonResponse({"error": "Delete object error."}, status=500)
    return JsonResponse({"error": "Недійсний метод запиту."}, status=405)



def get_object(request, item_id):
    """Представлення для отримання конкретного об'єкта за ID."""
    obj = NetworkHelper.get_item(item_id)
    if obj:
        return render(request, 'product_detail.html', {'object': obj})
    else:
        return render(request, 'error.html', {'message': 'Object not found.'})

def receipt_item(request):
    products = Product.objects.all()  # Отримуємо всі продукти для вибору
    return render(request, 'PharmacyInterface/receipt_item.html', {'products': products})


def submit_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))

        # Отримуємо товар з Product за його ID
        product = get_object_or_404(Product, product_id=product_id)

        # Перевіряємо, чи достатньо товару на складі
        if quantity > product.quantity_in_stock:
            messages.error(request, "Not enough product in stock")
            return render(request, 'PharmacyInterface/receipt_item.html', {'products': Product.objects.all()})

        # Створюємо запис у ReceiptItem
        ReceiptItem.objects.create(quantity=quantity)


        # Створюємо запис у Order без customer і warehouse_stock
        order = Order.objects.create(
            product=product,
            quantity=quantity,
            order_date=timezone.now()
        )

        product.quantity_in_stock -= quantity
        product.save()

        # Додавання повідомлення про успіх
        messages.success(request, 'Order successfully added to order list.')
        return redirect('PharmacyInterface:receipt_item')

    return redirect('PharmacyInterface:home')

def order_list(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    return render(request, 'PharmacyInterface/order_list.html', {'orders': orders, 'total_orders': total_orders})

def delete_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    order.delete()
    messages.success(request, 'Order successfully deleted.')
    return redirect('PharmacyInterface:order_list')

def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('PharmacyInterface:home')  # Перенаправлення на головну сторінку
    else:
        form = CustomerForm()
    return render(request, 'PharmacyInterface/customer_form.html', {'form': form})

def customer_list(request):
    customers = Customer.objects.all()  # Отримуємо всіх клієнтів з бази даних
    return render(request, 'PharmacyInterface/customer_list.html', {'customers': customers})

def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)
    customer.delete()
    messages.success(request, 'Customer successfully deleted.')
    return redirect('PharmacyInterface:customer_list')