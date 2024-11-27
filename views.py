from django.shortcuts import render
from django.utils import timezone

from pharmacyApp.repositories.product_repository import ProductRepository
from pharmacyApp.repositories.customer_repository import CustomerRepository
from pharmacyApp.repositories.receipt_item_repository import ReceiptItemRepository
from pharmacyApp.repositories.supplier_repository import SupplierRepository

from pharmacyApp.views import ReceiptItemViewSet
from pharmacyApp.views import SupplierViewSet
from types import SimpleNamespace      #сімпл дімпл папит сквіш

from django.shortcuts import redirect
from .forms import ProductForm , CustomerForm
from django.http import JsonResponse
from django.contrib import messages

from math import pi

import plotly.express as px
import plotly.io as pio

from bokeh.plotting import figure
from bokeh.embed import json_item
from bokeh.transform import cumsum
from bokeh.models import ColumnDataSource
import requests
from decimal import Decimal
from datetime import date
from pharmacyApp.serializers import SupplierSerializer
from pharmacyApp.models import Supplier

def home(request):
    return render(request, 'PharmacyInterface/home.html')


API_BASE_URL = "http://127.0.0.1:8000/api"
API_AUTH = ('yana_admin', 'yana2006')  # Логін і пароль для Basic Authentication


def product_list(request):
    response = requests.get(f"{API_BASE_URL}/products/", auth=API_AUTH)
    if response.status_code == 200:
        products = response.json()  # Має повертати список словників із даними продуктів
        return render(request, 'PharmacyInterface/product_list.html', {'products': products})
    else:
        return render(request, 'PharmacyInterface/error.html', {'message': 'Failed to fetch product list.'})


def product_detail(request, pk):
    response = requests.get(f"{API_BASE_URL}/products/{pk}/", auth=API_AUTH)
    if response.status_code == 200:
        product = response.json()  # Отримуємо дані продукту у вигляді словника
        return render(request, 'PharmacyInterface/product_detail.html', {'object': product})
    else:
        return render(request, 'PharmacyInterface/error.html', {'message': 'Failed to fetch product details.'})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Значення за замовчуванням для кількості в запасі
            if data.get('quantity_in_stock') is None:
                data['quantity_in_stock'] = 0

            # Серіалізація об'єктів, таких як Supplier
            if 'supplier' in data and isinstance(data['supplier'], Supplier):
                supplier = data['supplier']
                supplier_serializer = SupplierSerializer(supplier)
                data['supplier'] = supplier_serializer.data  # Замінюємо на серіалізовані дані

            # Серіалізація складних типів даних
            for key, value in data.items():
                if isinstance(value, Decimal):  # Перетворюємо Decimal у float
                    data[key] = float(value)
                elif isinstance(value, date):  # Перетворюємо date у ISO-формат
                    data[key] = value.isoformat()
                elif hasattr(value, 'id'):  # Якщо це об'єкт із полем 'id' (наприклад, інші моделі)
                    data[key] = value.id
                elif isinstance(value, (list, tuple)) and all(hasattr(item, 'id') for item in value):
                    # Для списків об'єктів з ID (наприклад, ManyToMany)
                    data[key] = [item.id for item in value]

            # Надсилаємо POST-запит до API
            try:
                response = requests.post(
                    f"{API_BASE_URL}/products/",
                    json=data,  # Передаємо дані у форматі JSON
                    auth=API_AUTH  # Аутентифікація
                )

                if response.status_code == 201:  # Код 201 означає успішне створення
                    messages.success(request, "Product created successfully!")
                    return redirect('PharmacyInterface:product_list')
                else:
                    # Обробка помилок API
                    try:
                        error_details = response.json()  # Отримуємо повідомлення про помилку
                    except ValueError:
                        error_details = {"error": "Unexpected response from API"}
                    messages.error(request, f"Failed to create product: {error_details}")
            except requests.RequestException as e:
                messages.error(request, f"An error occurred while creating the product: {str(e)}")
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = ProductForm()

    return render(request, 'PharmacyInterface/product_form.html', {'form': form})


def product_update(request, pk):
    # Отримуємо інформацію про продукт через API
    response = requests.get(f"{API_BASE_URL}/products/{pk}/", auth=API_AUTH)
    if response.status_code == 200:
        try:
            product = response.json()  # Отримуємо дані продукту у вигляді словника
        except requests.exceptions.JSONDecodeError:
            return render(request, 'PharmacyInterface/error.html', {'message': 'Invalid response from API.'})
    else:
        return render(request, 'PharmacyInterface/error.html', {'message': 'Failed to fetch product details.'})

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Перетворення даних для JSON
            data = {
                key: (
                    float(value) if isinstance(value, Decimal) else
                    value.isoformat() if isinstance(value, date) else
                    value.supplier_id if key == 'supplier' and hasattr(value, 'supplier_id') else
                    value
                )
                for key, value in data.items()
            }

            # Відправляємо PUT-запит до API
            update_response = requests.put(
                f"{API_BASE_URL}/products/{pk}/",
                json=data,  # Передаємо дані у форматі JSON
                auth=API_AUTH
            )

            if update_response.status_code == 200:
                return redirect('PharmacyInterface:product_detail', pk=pk)
            else:
                try:
                    error_details = update_response.json()
                except requests.exceptions.JSONDecodeError:
                    error_details = "API returned an invalid response."
                return render(request, 'PharmacyInterface/error.html', {
                    'message': 'Failed to update product.',
                    'details': error_details
                })

    else:
        form = ProductForm(initial=product)  # Передаємо початкові дані продукту в форму

    return render(request, 'PharmacyInterface/product_form.html', {'form': form})



def receipt_item(request):

    response = requests.get(f"{API_BASE_URL}/products/", auth=API_AUTH)
    if response.status_code == 200:
        products = response.json()  # Отримуємо список продуктів у вигляді словників
        return render(request, 'PharmacyInterface/receipt_item.html', {'products': products})
    else:
        return render(request, 'PharmacyInterface/error.html', {'message': 'Failed to fetch product list for receipt.'})


def order_list(request):
    response = requests.get(f"{API_BASE_URL}/receiptitems/", auth=API_AUTH)
    if response.status_code == 200:
        orders = response.json()
        total_orders = len(orders)
        total_price = sum(order['total_order_price'] for order in orders)

        return render(request, 'PharmacyInterface/order_list.html', {
            'orders': orders,
            'total_orders': total_orders,
            'total_price': total_price
        })
    else:
        return render(request, 'PharmacyInterface/error.html', {'message': 'Failed to fetch order list.'})


def delete_order(request, order_id):
    # Надсилаємо DELETE-запит до API
    response = requests.delete(
        f"{API_BASE_URL}/receiptitems/{order_id}/",  # Ендпоінт для видалення замовлення
        auth=API_AUTH  # Аутентифікація
    )

    if response.status_code == 204:  # Код 204 означає успішне видалення
        messages.success(request, 'Order successfully deleted.')
    else:
        # Перевіряємо, чи є тіло відповіді, і обробляємо помилки
        try:
            # Перевіряємо, чи є JSON у відповіді
            error_message = response.json().get('detail', 'Failed to delete order.')
        except ValueError:  # Якщо відповідь не є JSON (або порожня)
            error_message = 'Failed to delete order. No response from server.'

        messages.error(request, f"Error: {error_message}")

    # Повертаємо користувача до списку замовлень
    return redirect('PharmacyInterface:order_list')

def submit_order(request):
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product')
            quantity = int(request.POST.get('quantity'))
            receipt_id = request.POST.get('receipt_id')

            # Формуємо дані для запиту
            order_data = {
                'product': product_id,
                'quantity': quantity,
                'receipt_id': receipt_id,
                'order_date': timezone.now().isoformat(),
            }

            # Відправляємо POST-запит до API
            response = requests.post(
                f"{API_BASE_URL}/receiptitems/",
                json=order_data,
                auth=API_AUTH
            )

            if response.status_code == 201:
                messages.success(request, 'Order successfully added.')
                return redirect('PharmacyInterface:receipt_item')
            else:
                error_message = response.json().get('detail', 'Unknown error occurred.')
                messages.error(request, f"Error: {error_message}")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return redirect('PharmacyInterface:home')


def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            # Отримання даних із форми
            customer_data = form.cleaned_data

            # Надсилання POST-запиту до API
            response = requests.post(
                f"{API_BASE_URL}/customers/",  # Ендпоінт для створення клієнта
                json=customer_data,  # Дані у форматі JSON
                auth=API_AUTH  # Аутентифікація
            )

            if response.status_code == 201:  # 201 означає успішне створення
                return redirect('PharmacyInterface:home')
            else:
                # Перевіряємо, чи є JSON у відповіді
                try:
                    error_message = response.json().get('detail', 'Failed to create customer.')
                except ValueError:  # Якщо JSON не вдалося декодувати
                    error_message = f"Failed to create customer. Response status: {response.status_code}"
                form.add_error(None, error_message)
    else:
        form = CustomerForm()

    return render(request, 'PharmacyInterface/customer_form.html', {'form': form})


def customer_list(request):
    # Надсилаємо GET-запит до API для отримання списку клієнтів
    response = requests.get(
        f"{API_BASE_URL}/customers/",  # Ендпоінт для отримання клієнтів
        auth=API_AUTH  # Аутентифікація
    )

    if response.status_code == 200:  # Успішне отримання даних
        customers = response.json()  # Розбираємо JSON у Python-об'єкт
    else:
        # У разі помилки, створюємо пустий список і додаємо повідомлення
        customers = []
        messages.error(request, 'Failed to fetch customer list.')

    # Рендеримо шаблон із отриманими даними
    return render(request, 'PharmacyInterface/customer_list.html', {'customers': customers})


def delete_customer(request, customer_id):
    # Надсилаємо DELETE-запит до API
    response = requests.delete(
        f"{API_BASE_URL}/customers/{customer_id}/",  # Ендпоінт для видалення клієнта
        auth=API_AUTH  # Аутентифікація
    )

    if response.status_code == 204:  # Код 204 означає успішне видалення
        messages.success(request, 'Customer successfully deleted.')
    else:
        # Обробка помилки
        try:
            error_message = response.json().get('detail', 'Failed to delete customer.')
        except ValueError:  # Якщо відповідь не містить JSON
            error_message = f"Failed to delete customer. Response status: {response.status_code}"
        messages.error(request, f"Error: {error_message}")

    # Повернення користувача до списку клієнтів
    return redirect('PharmacyInterface:customer_list')


def object_list(request):
    products = ProductRepository().get_all()  # Отримуємо всі продукти через репозиторій
    return render(request, 'object_list.html', {'objects': products})


def delete_object(request, item_id):
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
    product = ProductRepository().get_by_id(item_id)  # Отримуємо продукт через репозиторій
    if product:
        return render(request, 'product_detail.html', {'object': product})
    else:
        return render(request, 'error.html', {'message': 'Object not found.'})


def popular_supplier_view(request):
    response = requests.get(f"{API_BASE_URL}/popular-supplier/", auth=API_AUTH)

    if response.status_code == 200:
        data = response.json()
        popular_supplier = data.get('popular_supplier', None)
        suppliers = data.get('suppliers', [])
    else:
        popular_supplier = None
        suppliers = []
        messages.error(request, 'Failed to fetch popular supplier data.')

    return render(request, 'PharmacyInterface/popular_supplier.html', {
        'popular_supplier': popular_supplier,
        'suppliers': suppliers
    })


def products_with_orders_view(request):
    response = requests.get(
        f"{API_BASE_URL}/products_with_orders/",  # Ендпоінт
        auth=API_AUTH
    )

    if response.status_code == 200:
        products_with_orders = response.json()
    else:
        products_with_orders = []
        messages.error(request, 'Failed to fetch products with orders.')

    return render(request, 'PharmacyInterface/products_with_orders.html', {
        'products_with_orders': products_with_orders
    })




#--------------------------------------------------------------------------------------------------------------
def dashboardPlotly(request):
    return render(request, 'PharmacyInterface/dashboardPlotly.html')


#products_with_order_count
def plotly_bar_chart_1(request):
    try:
        # Отримуємо параметр min_orders
        min_orders = int(request.GET.get('min_orders', 1))

        # Імітуємо об'єкт request із query_params
        mock_request = SimpleNamespace(query_params={"min_orders": min_orders})

        # Викликаємо функцію з PharmacyApp напряму
        receipt_item_view_set = ReceiptItemViewSet()
        data = receipt_item_view_set.products_with_order_count(mock_request)

        if not data["chart_data"]:  # Якщо даних немає
            return JsonResponse({"error": "No data available for bar chart"}, status=404)

        # Створення стовпчикового графіка
        fig = px.bar(data["chart_data"], x='product__name', y='order_count', title='Order Count by Product')

        # Серіалізація графіка
        fig_json = pio.to_json(fig)
        return JsonResponse(fig_json, safe=False)

    except Exception as e:
        # Логування помилки
        print(f"Error in plotly_bar_chart: {e}")
        return JsonResponse({"error": str(e)}, status=500)


#receiptitems_stats
def plotly_pie_chart_2(request):
    try:
        # Отримуємо параметри фільтрації з GET-запиту
        min_quantity = int(request.GET.get('min_quantity', 0))

        # Імітуємо об'єкт request із параметрами
        mock_request = SimpleNamespace(query_params={"min_quantity": min_quantity})

        # Викликаємо функцію з PharmacyApp напряму
        receipt_item_view_set = ReceiptItemViewSet()
        response_data = receipt_item_view_set.receiptitems_stats(mock_request)

        # Перевіряємо, чи є ключ 'chart_data'
        if "chart_data" not in response_data or not response_data["chart_data"]:
            return JsonResponse({"error": "No data available for pie chart"}, status=404)

        # Отримуємо та фільтруємо дані
        chart_data = response_data["chart_data"]
        filtered_data = [
            item for item in chart_data if item["quantity"] >= min_quantity
        ]
        print(f"Filtered data: {filtered_data}")  # Логування для діагностики

        if not filtered_data:
            return JsonResponse({"error": "No data matches the filter."}, status=404)

        # Підготовка даних для кругової діаграми
        names = [item["receipt_item_id"] for item in filtered_data]
        values = [item["quantity"] for item in filtered_data]

        # Створення кругової діаграми
        fig = px.pie(
            names=names,
            values=values,
            title=f'Quantity Distribution by Receipt Items (Min Quantity: {min_quantity})'
        )

        # Серіалізація графіка
        fig_json = pio.to_json(fig)
        return JsonResponse(fig_json, safe=False)

    except Exception as e:
        # Логування помилки
        print(f"Error in plotly_pie_chart_2_with_filter: {e}")
        return JsonResponse({"error": str(e)}, status=500)



#receiptitems_grouped_stats
def plotly_bar_chart_3(request):
    try:
        # Отримуємо параметри фільтрації з GET-запиту
        min_income = float(request.GET.get('min_income', 0))

        # Імітуємо об'єкт request із параметрами
        mock_request = SimpleNamespace(query_params={"min_income": min_income})

        # Викликаємо функцію з PharmacyApp напряму
        receipt_item_view_set = ReceiptItemViewSet()
        response_data = receipt_item_view_set.receiptitems_grouped_stats(mock_request)

        # Перевіряємо, чи є дані
        if "by_day" not in response_data or not response_data["by_day"]:
            return JsonResponse({"error": "No data available for bar chart"}, status=404)

        # Отримуємо та фільтруємо дані
        chart_data = response_data["by_day"]
        filtered_data = [
            item for item in chart_data if item["total_income"] >= min_income
        ]
        print(f"Filtered data: {filtered_data}")  # Логування для діагностики

        if not filtered_data:
            return JsonResponse({"error": "No data matches the filter."}, status=404)

        # Підготовка осей графіка
        days = [item["day"] for item in filtered_data]
        incomes = [item["total_income"] for item in filtered_data]

        # Створення стовпчастого графіка
        fig = px.bar(
            x=days,
            y=incomes,
            title='Filtered Daily Total Income' if min_income > 0 else 'Daily Total Income',
            labels={"x": "Day", "y": "Total Income"},
            text=incomes
        )
        fig.update_layout(
            xaxis_title='Day',
            yaxis_title='Total Income',
            xaxis=dict(type='category'),  # Використовуємо категорію для осі X
            uniformtext_minsize=8,
            uniformtext_mode='hide'
        )

        # Серіалізація графіка
        fig_json = pio.to_json(fig)
        return JsonResponse(fig_json, safe=False)

    except Exception as e:
        print(f"Error in plotly_bar_chart_3_no_pandas: {e}")
        return JsonResponse({"error": str(e)}, status=500)


#suppliers_with_product_count
def plotly_line_chart_4(request):
    try:
        # Отримуємо параметри фільтрації з GET-запиту
        min_supplied_products = int(request.GET.get('min_supplied_products', 0))

        # Імітуємо об'єкт request із параметрами
        mock_request = SimpleNamespace(query_params={"min_supplied_products": min_supplied_products})

        # Викликаємо функцію з PharmacyApp напряму
        supplier_view_set = SupplierViewSet()
        response_data = supplier_view_set.suppliers_with_product_count(mock_request)

        # Перевіряємо, чи є дані
        if "chart_data" not in response_data or not response_data["chart_data"]:
            return JsonResponse({"error": "No data available for line chart"}, status=404)

        # Отримуємо та фільтруємо дані
        chart_data = response_data["chart_data"]
        filtered_data = [
            item for item in chart_data if item["total_products"] >= min_supplied_products
        ]
        print(f"Filtered data: {filtered_data}")  # Логування для діагностики

        if not filtered_data:
            return JsonResponse({"error": "No data matches the filter."}, status=404)

        # Підготовка осей графіка
        supplier_names = [item["name"] for item in filtered_data]
        total_products = [item["total_products"] for item in filtered_data]

        # Створення лінійної діаграми
        fig = px.line(
            x=supplier_names,
            y=total_products,
            title=f'Filtered Number of Products Supplied by Suppliers (Min Products: {min_supplied_products})'
                  if min_supplied_products > 0 else 'Number of Products Supplied by Suppliers',
            labels={"x": "Supplier Name", "y": "Total Products"},
            markers=True  # Додавання маркерів на лінії
        )
        fig.update_layout(
            xaxis_title='Supplier Name',
            yaxis_title='Total Products',
            xaxis=dict(tickangle=-45)  # Нахил підписів на осі X
        )

        # Серіалізація графіка
        fig_json = pio.to_json(fig)
        return JsonResponse(fig_json, safe=False)

    except Exception as e:
        # Логування помилки
        print(f"Error in plotly_line_chart_4: {e}")
        return JsonResponse({"error": str(e)}, status=500)


# suppliers_stats
def plotly_pie_chart_5(request):
    try:
        # Отримуємо параметри фільтрації з GET-запиту
        min_products = int(request.GET.get('min_products', 0))

        # Імітуємо об'єкт request із параметрами
        mock_request = SimpleNamespace(query_params={"min_products": min_products})

        # Викликаємо функцію з PharmacyApp напряму
        supplier_view_set = SupplierViewSet()
        response_data = supplier_view_set.suppliers_stats(mock_request)

        # Перевіряємо, чи є ключ 'chart_data'
        if "chart_data" not in response_data or not response_data["chart_data"]:
            return JsonResponse({"error": "No data available for pie chart"}, status=404)

        # Отримуємо та фільтруємо дані
        chart_data = response_data["chart_data"]
        filtered_data = [
            item for item in chart_data if item["total_products"] >= min_products
        ]
        print(f"Filtered data: {filtered_data}")  # Логування для діагностики

        if not filtered_data:
            return JsonResponse({"error": "No data matches the filter."}, status=404)

        # Підготовка даних для кругової діаграми
        names = [item["name"] for item in filtered_data]
        values = [item["total_products"] for item in filtered_data]

        # Створення кругової діаграми
        fig = px.pie(
            names=names,
            values=values,
            title=f'Distribution of Total Products by Suppliers (Min Products: {min_products})'
        )
        fig.update_layout(
            title={
                "text": f'Distribution of Total Products by Suppliers (Min Products: {min_products})',
                "x": 0.5,
                "xanchor": "center"
            }
        )

        # Серіалізація графіка
        fig_json = pio.to_json(fig)
        return JsonResponse(fig_json, safe=False)

    except Exception as e:
        # Логування помилки
        print(f"Error in plotly_pie_chart_5: {e}")
        return JsonResponse({"error": str(e)}, status=500)


def plotly_area_chart_6(request):
    try:
        # Отримуємо параметри фільтрації з GET-запиту
        min_total_products = int(request.GET.get('min_total_products', 0))

        # Імітуємо об'єкт request із параметрами
        mock_request = SimpleNamespace(query_params={"min_total_products": min_total_products})

        # Викликаємо функцію з PharmacyApp напряму
        supplier_view_set = SupplierViewSet()
        response_data = supplier_view_set.suppliers_grouped_stats(mock_request)

        # Перевіряємо, чи є ключ 'by_total_products'
        if "by_total_products" not in response_data or not response_data["by_total_products"]:
            return JsonResponse({"error": "No data available for area chart"}, status=404)

        # Отримуємо та фільтруємо дані
        chart_data = response_data["by_total_products"]
        filtered_data = [
            item for item in chart_data if item["total_products"] >= min_total_products
        ]
        print(f"Filtered data: {filtered_data}")  # Логування для діагностики

        if not filtered_data:
            return JsonResponse({"error": "No data matches the filter."}, status=404)

        # Підготовка осей графіка
        total_products = [item["total_products"] for item in filtered_data]
        total_suppliers = [item["total_suppliers"] for item in filtered_data]

        # Створення графіка зони
        fig = px.area(
            x=total_products,
            y=total_suppliers,
            title=f'Suppliers Count by Total Products (Min Total Products: {min_total_products})'
                  if min_total_products > 0 else 'Suppliers Count by Total Products',
            labels={'x': 'Total Products', 'y': 'Total Suppliers'}
        )
        fig.update_layout(
            xaxis_title='Total Products',
            yaxis_title='Number of Suppliers',
            template='plotly_white'
        )

        # Серіалізація графіка
        fig_json = pio.to_json(fig)
        return JsonResponse(fig_json, safe=False)

    except Exception as e:
        # Логування помилки
        print(f"Error in plotly_area_chart_6: {e}")
        return JsonResponse({"error": str(e)}, status=500)



#------------------------------------------------------------------------------------------------------------------------
def dashboardBokeh(request):
    return render(request, 'PharmacyInterface/dashboardBokeh.html')


#products_with_order_count
def bokeh_bar_chart_1(request):
    try:
        # Отримуємо параметр min_orders із запиту
        min_orders = int(request.GET.get('min_orders', 1))

        # Імітуємо об'єкт request із query_params
        mock_request = SimpleNamespace(query_params={"min_orders": min_orders})

        # Викликаємо функцію з PharmacyApp напряму
        receipt_item_view_set = ReceiptItemViewSet()
        data = receipt_item_view_set.products_with_order_count(mock_request)

        if not data["chart_data"]:  # Якщо даних немає
            return JsonResponse({"error": "No data available for bar chart"}, status=404)

        # Дані для побудови графіка
        chart_data = data["chart_data"]
        product_names = [item["product__name"] for item in chart_data]
        order_counts = [item["order_count"] for item in chart_data]

        # Додавання кольорів для стовпців
        from bokeh.palettes import Category20
        palette = Category20[max(3, len(product_names))]  # Динамічний вибір кольорів
        colors = [palette[i % len(palette)] for i in range(len(product_names))]

        # Підготовка даних для Bokeh
        source = ColumnDataSource(data=dict(
            product__name=product_names,
            order_count=order_counts,
            color=colors
        ))

        # Створення стовпчастої діаграми
        p = figure(
            x_range=product_names,
            height=500, width=800,
            title="Order Count by Product",
            toolbar_location=None,
            tools="hover",
            tooltips="@product__name: @order_count"
        )

        p.vbar(
            x='product__name',
            top='order_count',
            width=0.8,
            color='color',
            source=source
        )

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.xaxis.axis_label = "Products"
        p.yaxis.axis_label = "Order Count"
        p.xaxis.major_label_orientation = 0.8

        # Серіалізація графіка
        return JsonResponse(json_item(p), safe=False)

    except Exception as e:
        print(f"Error in bokeh_bar_chart_1: {e}")
        return JsonResponse({"error": str(e)}, status=500)

#receiptitems_stats
def bokeh_pie_chart_2(request):
    try:
        # Отримання параметра фільтрації
        min_quantity = int(request.GET.get('min_quantity', 1))
        print(f"Filtering with min_quantity: {min_quantity}")  # Діагностика

        # Імітуємо запит із параметрами
        mock_request = SimpleNamespace(query_params={"min_quantity": min_quantity})
        receipt_item_view_set = ReceiptItemViewSet()
        response_data = receipt_item_view_set.receiptitems_stats(mock_request)

        # Перевіряємо наявність даних
        if "chart_data" not in response_data or not response_data["chart_data"]:
            return JsonResponse({"error": "No data available for pie chart"}, status=404)

        # Дані для кругової діаграми
        chart_data = response_data["chart_data"]
        filtered_data = [item for item in chart_data if item["quantity"] >= min_quantity]
        print(f"Filtered data: {filtered_data}")  # Діагностика

        if not filtered_data:
            return JsonResponse({"error": "No data matches the filter."}, status=404)

        # Підготовка даних для графіка
        receipt_items = [item["receipt_item_id"] for item in filtered_data]
        quantities = [item["quantity"] for item in filtered_data]
        total_quantity = sum(quantities)
        angles = [q / total_quantity * 2 * pi for q in quantities]

        # Додавання кольорів
        from bokeh.palettes import Category20c
        colors = Category20c[len(receipt_items)]

        # Формування даних для Bokeh
        source = ColumnDataSource(data=dict(
            receipt_item_id=receipt_items,
            quantity=quantities,
            angle=angles,
            color=colors
        ))

        # Створення графіка
        p = figure(
            height=500, width=500,
            title="Filtered Quantity Distribution by Receipt Items",
            toolbar_location=None,
            tools="hover",
            tooltips="@receipt_item_id: @quantity", x_range=(-0.5, 1.0)
        )

        p.wedge(
            x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True),
            end_angle=cumsum('angle'),
            line_color="white", fill_color='color',
            legend_field='receipt_item_id', source=source
        )

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        # Серіалізація графіка
        return JsonResponse(json_item(p), safe=False)

    except Exception as e:
        print(f"Error in bokeh_pie_chart_2: {e}")
        return JsonResponse({"error": str(e)}, status=500)


#receiptitems_grouped_stats
def bokeh_bar_chart_3(request):
    try:
        # Отримуємо параметри фільтрації з GET-запиту
        min_income = float(request.GET.get('min_income', 0))
        category = request.GET.get('category', None)  # Фільтр за категорією, якщо задано

        # Імітуємо об'єкт request із параметрами
        mock_request = SimpleNamespace(query_params={"min_income": min_income, "category": category})
        receipt_item_view_set = ReceiptItemViewSet()
        response_data = receipt_item_view_set.receiptitems_grouped_stats(mock_request)

        # Перевіряємо, чи є дані
        if "by_day" not in response_data or not response_data["by_day"]:
            return JsonResponse({"error": "No data available for bar chart"}, status=404)

        # Отримуємо дані
        chart_data = response_data["by_day"]

        # Фільтрація за мінімальним доходом
        filtered_data = [item for item in chart_data if float(item["total_income"]) >= min_income]
        print(f"Filtered data: {filtered_data}")  # Логування для діагностики

        if not filtered_data:
            return JsonResponse({"error": "No data matches the filter."}, status=404)

        # Підготовка списків для графіка
        days = [item["day"] for item in filtered_data]
        total_income = [float(item["total_income"]) for item in filtered_data]  # Конвертація Decimal у float

        # Форматування дат у вигляді строк
        formatted_days = [str(day) for day in days]

        # Підготовка даних для Bokeh
        source = ColumnDataSource(data=dict(
            day=formatted_days,  # Перетворені строки дат
            total_income=total_income
        ))

        # Створення графіка
        p = figure(
            x_range=source.data['day'],
            height=500, width=800,
            title="Filtered Daily Total Income" if min_income > 0 else "Daily Total Income",
            toolbar_location=None,
            tools="hover",
            tooltips="@day: @total_income"
        )

        p.vbar(
            x='day',
            top='total_income',
            width=0.8,
            source=source
        )

        p.xaxis.axis_label = "Day"
        p.yaxis.axis_label = "Total Income"
        p.xaxis.major_label_orientation = 0.8
        p.y_range.start = 0
        p.xgrid.grid_line_color = None

        # Серіалізація графіка
        return JsonResponse(json_item(p), safe=False)

    except Exception as e:
        print(f"Error in bokeh_bar_chart_3: {e}")
        return JsonResponse({"error": str(e)}, status=500)

#suppliers_with_product_count
def bokeh_line_chart_4(request):
    try:
        # Отримуємо параметри фільтрації з GET-запиту
        min_supplied_products = int(request.GET.get('min_supplied_products', 0))

        # Імітуємо об'єкт request із параметрами
        mock_request = SimpleNamespace(query_params={"min_supplied_products": min_supplied_products})

        # Викликаємо функцію з PharmacyApp напряму
        supplier_view_set = SupplierViewSet()
        response_data = supplier_view_set.suppliers_with_product_count(mock_request)

        # Перевіряємо, чи є дані
        if "chart_data" not in response_data or not response_data["chart_data"]:
            return JsonResponse({"error": "No data available for line chart"}, status=404)

        # Отримуємо та фільтруємо дані для лінійної діаграми
        chart_data = response_data["chart_data"]
        filtered_data = [item for item in chart_data if item["total_products"] >= min_supplied_products]
        print(f"Filtered data: {filtered_data}")  # Логування для діагностики

        if not filtered_data:
            return JsonResponse({"error": "No data matches the filter."}, status=404)

        # Підготовка списків для графіка
        supplier_names = [item["name"] for item in filtered_data]
        total_products = [item["total_products"] for item in filtered_data]

        # Підготовка даних для Bokeh
        source = ColumnDataSource(data=dict(
            supplier_names=supplier_names,
            total_products=total_products
        ))

        # Створення лінійного графіка
        p = figure(
            height=500, width=800,
            title="Filtered Number of Products Supplied by Suppliers" if min_supplied_products > 0 else "Number of Products Supplied by Suppliers",
            toolbar_location=None,
            tools="hover",
            tooltips="@supplier_names: @total_products Products"
        )

        # Додавання лінії на графік
        p.line(
            x=list(range(len(supplier_names))),
            y=total_products,
            line_width=2,
            color="blue",
            legend_label="Total Products"
        )

        # Додавання маркерів
        p.scatter(
            x=list(range(len(supplier_names))),
            y=total_products,
            size=8,
            color="red",
            legend_label="Total Products"
        )

        # Налаштування осей
        p.xaxis.axis_label = "Supplier Name"
        p.xaxis.ticker = list(range(len(supplier_names)))
        p.xaxis.major_label_overrides = {i: name for i, name in enumerate(supplier_names)}
        p.yaxis.axis_label = "Total Products"

        p.xgrid.grid_line_color = None
        p.legend.location = "top_left"

        # Серіалізація графіка
        return JsonResponse(json_item(p), safe=False)

    except Exception as e:
        print(f"Error in bokeh_line_chart_4: {e}")
        return JsonResponse({"error": str(e)}, status=500)


#suppliers_stats
def bokeh_pie_chart_5(request):
    try:
        print("Fetching supplier stats data from repository...")

        # Отримуємо параметр мінімальної кількості продуктів
        min_products = int(request.GET.get('min_products', 0))
        print(f"Minimum products filter: {min_products}")  # Логування для діагностики

        # Імітуємо об'єкт request із параметрами
        mock_request = SimpleNamespace(query_params={"min_products": min_products})
        supplier_view_set = SupplierViewSet()
        response_data = supplier_view_set.suppliers_stats(mock_request)

        # Перевіряємо, чи є дані
        if "chart_data" not in response_data or not response_data["chart_data"]:
            print("No data available in response")
            return JsonResponse({"error": "No data available for pie chart"}, status=404)

        # Фільтрація даних за мінімальною кількістю продуктів
        chart_data = response_data["chart_data"]
        filtered_data = [item for item in chart_data if item["total_products"] >= min_products]
        print(f"Filtered data: {filtered_data}")  # Логування для діагностики

        if not filtered_data:
            print("Filtered data is empty")
            return JsonResponse({"error": "No data matches the filter."}, status=404)

        # Підготовка даних для Bokeh
        supplier_names = [item["name"] for item in filtered_data]
        total_products = [item["total_products"] for item in filtered_data]
        total_sum = sum(total_products)
        angles = [prod / total_sum * 2 * pi for prod in total_products]

        # Додавання кольорів
        from bokeh.palettes import Category20c
        max_colors = len(Category20c)
        colors = Category20c[min(len(filtered_data), max_colors)]

        source = ColumnDataSource(data=dict(
            name=supplier_names,
            total_products=total_products,
            angle=angles,
            color=colors[:len(filtered_data)]  # Гарантія, що розмір палітри відповідає кількості даних
        ))

        # Створення кругової діаграми
        p = figure(
            height=500, width=500,
            title="Filtered Distribution of Total Products by Suppliers",
            toolbar_location=None,
            tools="hover",
            tooltips="@name: @total_products"
        )

        p.wedge(
            x=0, y=0,
            radius=0.4,
            start_angle=cumsum('angle', include_zero=True),
            end_angle=cumsum('angle'),
            line_color="white",
            fill_color='color',
            legend_field='name',
            source=source
        )

        p.legend.orientation = "vertical"
        p.legend.location = "top_right"
        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        print("Serializing pie chart...")
        return JsonResponse(json_item(p), safe=False)

    except Exception as e:
        print(f"Error in bokeh_pie_chart_5: {e}")
        return JsonResponse({"error": str(e)}, status=500)

#suppliers_grouped_stats
def bokeh_area_chart_6(request):
    try:
        print("Fetching grouped supplier stats data from repository...")

        # Отримуємо параметр мінімальної кількості продуктів
        min_total_products = int(request.GET.get('min_total_products', 0))
        print(f"Minimum total products filter: {min_total_products}")

        # Імітуємо об'єкт request із параметрами
        mock_request = SimpleNamespace(query_params={"min_total_products": min_total_products})
        supplier_view_set = SupplierViewSet()
        response_data = supplier_view_set.suppliers_stats(mock_request)

        # Перевіряємо, чи є дані
        if "chart_data" not in response_data or not response_data["chart_data"]:
            print("No data available in response")
            return JsonResponse({"error": "No data available for area chart"}, status=404)

        # Фільтрація даних за мінімальною кількістю продуктів
        chart_data = response_data["chart_data"]
        filtered_data = [item for item in chart_data if item["total_products"] >= min_total_products]
        print(f"Filtered data: {filtered_data}")

        if not filtered_data:
            print("Filtered data is empty")
            return JsonResponse({"error": "No data matches the filter."}, status=404)

        # Групування даних
        grouped_data = {}
        for item in filtered_data:
            total_products = item["total_products"]
            if total_products not in grouped_data:
                grouped_data[total_products] = {"total_suppliers": 0, "total_products_sum": 0}
            grouped_data[total_products]["total_suppliers"] += 1
            grouped_data[total_products]["total_products_sum"] += total_products

        # Перетворення у список для сортування
        grouped_list = [
            {
                "total_products": total_products,
                "total_suppliers": group["total_suppliers"],
                "average_products": group["total_products_sum"] / group["total_suppliers"],
            }
            for total_products, group in grouped_data.items()
        ]

        # Сортування за кількістю постачальників
        grouped_list = sorted(grouped_list, key=lambda x: x["total_suppliers"], reverse=True)
        print(f"Grouped data: {grouped_list}")

        # Підготовка даних для Bokeh
        total_products = [item["total_products"] for item in grouped_list]
        total_suppliers = [item["total_suppliers"] for item in grouped_list]

        # Створення графіка області
        print("Creating area chart...")
        p = figure(
            height=500, width=800,
            title="Suppliers Distribution by Total Products",
            toolbar_location=None,
            tools="hover",
            tooltips="@x: @y Suppliers"
        )

        # Додавання області
        p.varea(
            x=total_products,
            y1=0,
            y2=total_suppliers,
            fill_color="blue",
            fill_alpha=0.5,
        )

        # Додавання лінії
        p.line(
            x=total_products,
            y=total_suppliers,
            line_width=2,
            color="blue",
            legend_label="Total Suppliers"
        )

        # Налаштування осей
        p.xaxis.axis_label = "Total Products"
        p.yaxis.axis_label = "Total Suppliers"
        p.xgrid.grid_line_color = None
        p.legend.location = "top_left"

        # Серіалізація графіка
        print("Serializing chart...")
        return JsonResponse(json_item(p), safe=False)

    except Exception as e:
        print(f"Error in bokeh_area_chart_6: {e}")
        return JsonResponse({"error": str(e)}, status=500)

#--------------------------------------------------------------------------------------------------------------------------------
