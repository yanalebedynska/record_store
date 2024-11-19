from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, F

from pharmacyApp.repositories.product_repository import ProductRepository
from pharmacyApp.repositories.customer_repository import CustomerRepository
from pharmacyApp.repositories.receipt_item_repository import ReceiptItemRepository
from pharmacyApp.repositories.supplier_repository import SupplierRepository

from django.shortcuts import redirect
from .forms import ProductForm , CustomerForm
from django.http import JsonResponse
from django.contrib import messages

from math import pi
import pandas as pd

import plotly.express as px
import plotly.io as pio

from bokeh.plotting import figure
from bokeh.embed import json_item
from bokeh.transform import cumsum
from bokeh.palettes import Category20c
from bokeh.palettes import Category20
from bokeh.transform import factor_cmap

from bokeh.models import ColumnDataSource


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
    repository = ReceiptItemRepository()
    orders = repository.get_orders_sorted_by_date()

    total_orders = orders.count()

    total_price = orders.aggregate(
        total_price=Sum(F('product__price') * F('quantity'))
    )['total_price'] or 0

    return render(request, 'PharmacyInterface/order_list.html', {
        'orders': orders,
        'total_orders': total_orders,
        'total_price': total_price,
    })

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


def popular_supplier_view(request):
    repository = SupplierRepository()

    suppliers = repository.get_suppliers_with_product_count()

    popular_supplier = suppliers[0] if suppliers else None

    return render(request, 'PharmacyInterface/popular_supplier.html', {
        'popular_supplier': popular_supplier,
        'suppliers': suppliers
    })


def products_with_orders_view(request):
    repository = ReceiptItemRepository()
    products_with_orders = repository.get_products_with_order_count(min_orders=2)
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

        # Отримуємо дані через репозиторій
        repository = ReceiptItemRepository()
        queryset = repository.get_products_with_order_count(min_orders)

        # Перетворення даних у DataFrame
        data = list(queryset)
        if not data:  # Якщо даних немає, повертаємо помилку
            return JsonResponse({"error": "No data available for bar chart"}, status=404)

        df = pd.DataFrame(data)

        # Створення стовпчикового графіка
        fig = px.bar(df, x='product__name', y='order_count', title='Order Count by Product')

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
        # Отримуємо всі дані через репозиторій
        repository = ReceiptItemRepository()
        queryset = repository.get_all()

        # Перетворення даних у DataFrame
        data = queryset.values('receipt_item_id', 'quantity', 'product__price')
        df = pd.DataFrame(list(data))

        # Перевірка, чи є дані
        if df.empty:
            return JsonResponse({"error": "No data available for pie chart"}, status=404)

        # Створення кругової діаграми на основі кількості
        df_grouped = df.groupby('receipt_item_id').sum().reset_index()
        fig = px.pie(df_grouped, names='receipt_item_id', values='quantity', title='Quantity Distribution by Receipt Items')

        # Серіалізація графіка
        fig_json = pio.to_json(fig)
        return JsonResponse(fig_json, safe=False)

    except Exception as e:
        # Логування помилки
        print(f"Error in plotly_pie_chart_2: {e}")
        return JsonResponse({"error": str(e)}, status=500)


#receiptitems_grouped_stats
def plotly_bar_chart_3(request):
    try:
        # Отримуємо всі дані через репозиторій
        repository = ReceiptItemRepository()
        queryset = repository.get_all()

        # Перетворення даних у DataFrame
        data = queryset.values('product__category', 'order_date', 'quantity', 'product__price')
        df = pd.DataFrame(list(data))

        # Перевірка, чи є дані
        if df.empty:
            return JsonResponse({"error": "No data available for bar chart"}, status=404)

        # Перетворення дати в формат дня
        df['day'] = pd.to_datetime(df['order_date']).dt.strftime('%Y-%m-%d')

        # Додавання нового стовпця з загальною вартістю
        df['total_income'] = df['quantity'] * df['product__price']

        # Групування по днях
        day_group = df.groupby('day').agg(
            total_income=('total_income', 'sum'),
            total_quantity=('quantity', 'sum')
        ).reset_index()

        # Створення стовпчастого графіка
        fig = px.bar(
            day_group,
            x='day',
            y='total_income',
            title='Daily Total Income',
            text='total_income',  # Відображення значень на стовпцях
        )
        fig.update_layout(
            xaxis_title='Day',
            yaxis_title='Total Income',
            uniformtext_minsize=8,
            uniformtext_mode='hide'
        )

        # Серіалізація графіка
        fig_json = pio.to_json(fig)
        return JsonResponse(fig_json, safe=False)

    except Exception as e:
        # Логування помилки
        print(f"Error in plotly_bar_chart_daily: {e}")
        return JsonResponse({"error": str(e)}, status=500)


#suppliers_with_product_count
def plotly_line_chart_4(request):
    try:
        # Отримуємо всі дані через репозиторій
        repository = SupplierRepository()
        queryset = repository.get_suppliers_with_product_count()

        # Перетворення даних у DataFrame
        data = queryset.values('supplier_id', 'name', 'total_products')
        df = pd.DataFrame(list(data))

        # Перевірка, чи є дані
        if df.empty:
            return JsonResponse({"error": "No data available for line chart"}, status=404)

        # Створення лінійної діаграми
        fig = px.line(
            df,
            x='name',
            y='total_products',
            title='Number of Products Supplied by Suppliers',
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
        print(f"Error in plotly_line_chart_suppliers: {e}")
        return JsonResponse({"error": str(e)}, status=500)



#suppliers_stats
def plotly_pie_chart_5(request):
    try:
        # Отримуємо дані через репозиторій
        repository = SupplierRepository()
        queryset = repository.get_suppliers_with_product_count()

        # Перетворення даних у DataFrame
        data = queryset.values('supplier_id', 'name', 'total_products')
        df = pd.DataFrame(list(data))

        # Перевірка, чи є дані
        if df.empty:
            return JsonResponse({"error": "No data available for pie chart"}, status=404)

        # Створення кругової діаграми
        fig = px.pie(
            df,
            names='name',  # Використовуємо назву постачальника для підписів
            values='total_products',  # Загальна кількість продуктів
            title='Distribution of Total Products by Suppliers'
        )

        # Серіалізація графіка
        fig_json = pio.to_json(fig)
        return JsonResponse(fig_json, safe=False)

    except Exception as e:
        # Логування помилки
        print(f"Error in plotly_pie_chart_suppliers_stats: {e}")
        return JsonResponse({"error": str(e)}, status=500)

#suppliers_grouped_stats
def plotly_area_chart_6(request):
    try:
        # Отримуємо дані через репозиторій
        repository = SupplierRepository()
        queryset = repository.get_suppliers_with_product_count()

        # Перетворення даних у DataFrame
        data = queryset.values('supplier_id', 'name', 'total_products')
        df = pd.DataFrame(list(data))

        # Перевірка, чи є дані
        if df.empty:
            return JsonResponse({"error": "No data available for area chart"}, status=404)

        # Групування по кількості продуктів
        product_group = df.groupby('total_products').agg(
            total_suppliers=('supplier_id', 'count'),
            average_products=('total_products', 'mean')
        ).reset_index()

        product_group = product_group.sort_values(by='total_products', ascending=True)

        # Створення графіка зони
        fig = px.area(
            product_group,
            x='total_products',
            y='total_suppliers',
            title='Suppliers Count by Total Products',
            labels={'total_products': 'Total Products', 'total_suppliers': 'Total Suppliers'}
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
        print(f"Error in plotly_area_chart_suppliers_grouped: {e}")
        return JsonResponse({"error": str(e)}, status=500)

#------------------------------------------------------------------------------------------------------------------------
def dashboardBokeh(request):
    return render(request, 'PharmacyInterface/dashboardBokeh.html')


#products_with_order_count
def bokeh_bar_chart_1(request):
    try:
        # Отримуємо параметр min_orders з запиту
        min_orders = int(request.GET.get('min_orders', 1))

        # Отримуємо дані через репозиторій
        repository = ReceiptItemRepository()
        queryset = repository.get_products_with_order_count(min_orders)

        # Перетворення даних у DataFrame
        data = list(queryset)
        if not data:  # Якщо даних немає, повертаємо помилку
            return JsonResponse({"error": "No data available for bar chart"}, status=404)

        df = pd.DataFrame(data)

        # Додавання кольорів для стовпців
        from bokeh.palettes import Category20
        palette = Category20[max(3, len(df))]  # Динамічний вибір кольорів
        df['color'] = [palette[i % len(palette)] for i in range(len(df))]

        # Підготовка даних для Bokeh
        source = ColumnDataSource(df)

        # Створення стовпчастої діаграми
        p = figure(
            x_range=df['product__name'].tolist(),
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
        # Отримуємо параметр min_quantity з запиту
        min_quantity = int(request.GET.get('min_quantity', 1))

        # Отримуємо дані через репозиторій
        repository = ReceiptItemRepository()
        queryset = repository.get_all()

        # Перетворення даних у DataFrame
        data = queryset.values('receipt_item_id', 'quantity', 'product__price')
        df = pd.DataFrame(list(data))

        # Перевірка, чи є дані
        if df.empty:
            return JsonResponse({"error": "No data available for pie chart"}, status=404)

        # Фільтрація за min_quantity
        df = df[df['quantity'] >= min_quantity]

        # Обчислення часток
        df_grouped = df.groupby('receipt_item_id')['quantity'].sum().reset_index()
        df_grouped['angle'] = df_grouped['quantity'] / df_grouped['quantity'].sum() * 2 * pi
        df_grouped['color'] = Category20c[len(df_grouped)]

        # Створення кругової діаграми
        p = figure(height=500, width=500, title="Filtered Receipt Items Distribution by Quantity",
                   toolbar_location=None, tools="hover", tooltips="@receipt_item_id: @quantity", x_range=(-0.5, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True),
                end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend_field='receipt_item_id', source=df_grouped)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        return JsonResponse(json_item(p), safe=False)

    except Exception as e:
        print(f"Error in bokeh_pie_chart_2: {e}")
        return JsonResponse({"error": str(e)}, status=500)



#receiptitems_grouped_stats
def bokeh_bar_chart_3(request):
    try:
        # Отримуємо параметри
        min_income = float(request.GET.get('min_income', 0))
        category = request.GET.get('category', None)  # Новий параметр для фільтрації за категорією

        # Отримуємо дані через репозиторій
        repository = ReceiptItemRepository()
        queryset = repository.get_all()
        data = queryset.values('product__category', 'order_date', 'quantity', 'product__price')
        df = pd.DataFrame(list(data))

        if df.empty:
            return JsonResponse({"error": "No data available for bar chart"}, status=404)

        # Обчислення total_income
        df['total_income'] = df['quantity'] * df['product__price']
        df['total_income'] = df['total_income'].astype(float)  # Конвертація у float

        # Групування за категоріями
        category_group = df.groupby('product__category').agg(total_income=('total_income', 'sum')).reset_index()

        # Фільтрація за категорією
        if category and category != "all":
            category_group = category_group[category_group['product__category'] == category]

        # Фільтрація за min_income
        if min_income > 0:
            category_group = category_group[category_group['total_income'] >= min_income]

        if category_group.empty:
            return JsonResponse({"error": "No data matches the filter."}, status=404)

        # Додавання кольорів для графіка
        from bokeh.palettes import Category20
        palette = Category20[max(3, len(category_group))]
        category_group['color'] = [palette[i % len(palette)] for i in range(len(category_group))]

        # Створення графіка
        p = figure(
            x_range=category_group['product__category'].tolist(),
            height=500, width=800,
            title="Filtered Total Income by Product Category" if min_income > 0 else "Total Income by Product Category",
            toolbar_location=None,
            tools="hover",
            tooltips="@product__category: @total_income"
        )

        p.vbar(
            x='product__category',
            top='total_income',
            width=0.8,
            color='color',
            source=ColumnDataSource(category_group)
        )

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.xaxis.axis_label = "Product Categories"
        p.yaxis.axis_label = "Total Income"
        p.xaxis.major_label_orientation = 0.8

        return JsonResponse(json_item(p), safe=False)

    except Exception as e:
        print(f"Error in bokeh_bar_chart_3: {e}")
        return JsonResponse({"error": str(e)}, status=500)


#suppliers_with_product_count
def bokeh_line_chart_4(request):
    try:
        print("Fetching supplier data from repository...")
        repository = SupplierRepository()
        queryset = repository.get_suppliers_with_product_count()

        # Отримуємо параметр фільтра
        min_supplied_products = int(request.GET.get('min_supplied_products', 0))

        data = queryset.values('supplier_id', 'name', 'total_products')
        df = pd.DataFrame(list(data))

        if df.empty:
            print("No data available in DataFrame")
            return JsonResponse({"error": "No data available for line chart"}, status=404)

        # Фільтрація за мінімальною кількістю продуктів
        df = df[df['total_products'] >= min_supplied_products]

        # Конвертація total_products у float для сумісності
        df['total_products'] = df['total_products'].astype(float)

        print("Creating line chart...")
        p = figure(
            height=500, width=800,
            title="Total Products Supplied by Each Supplier",
            toolbar_location=None,
            tools="hover",
            tooltips="@name: @total_products Products"
        )

        # Додавання лінії на графік
        p.line(
            x=list(range(len(df))),
            y=df['total_products'],
            line_width=2,
            color="blue",
            legend_label="Total Products"
        )

        # Додавання маркерів
        p.scatter(
            x=list(range(len(df))),
            y=df['total_products'],
            size=8,
            color="red",
            legend_label="Total Products"
        )

        # Налаштування осей
        p.xaxis.axis_label = "Supplier Name"
        p.xaxis.ticker = list(range(len(df)))
        p.xaxis.major_label_overrides = {i: name for i, name in enumerate(df['name'])}
        p.yaxis.axis_label = "Total Products"

        p.xgrid.grid_line_color = None
        p.legend.location = "top_left"

        print("Serializing chart...")
        return JsonResponse(json_item(p), safe=False)

    except Exception as e:
        print(f"Error in bokeh_line_chart_4: {e}")
        return JsonResponse({"error": str(e)}, status=500)

#suppliers_stats
def bokeh_pie_chart_5(request):
    try:
        print("Fetching supplier stats data from repository...")

        min_products = int(request.GET.get('min_products', 0))  # Новий параметр фільтра
        print(f"Minimum products filter: {min_products}")

        repository = SupplierRepository()  # Використовується ваш репозиторій постачальників
        queryset = repository.get_suppliers_with_product_count()
        data = list(queryset.values('supplier_id', 'name', 'total_products'))
        print(f"Fetched data: {data}")

        if not data:
            print("No data available in queryset")
            return JsonResponse({"error": "No data available for pie chart"}, status=404)

        df = pd.DataFrame(data)
        print(f"DataFrame created: {df}")

        # Фільтрація за мінімальною кількістю продуктів
        df = df[df['total_products'] >= min_products]
        print(f"Filtered DataFrame: {df}")

        if df.empty:
            print("Filtered DataFrame is empty")
            return JsonResponse({"error": "No data matches the filter."}, status=404)

        # Додавання кольорів для графіка
        palette_size = max(3, len(df))  # Мінімум 3 кольори
        df['color'] = Category20c[palette_size][:len(df)]

        # Додавання часток для кругової діаграми
        df['angle'] = df['total_products'] / df['total_products'].sum() * 2 * pi

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
            source=df
        )

        p.legend.orientation = "vertical"
        p.legend.location = "top_right"
        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        return JsonResponse(json_item(p), safe=False)

    except Exception as e:
        print(f"Error in bokeh_pie_chart_suppliers: {e}")
        return JsonResponse({"error": str(e)}, status=500)

#suppliers_grouped_stats
def bokeh_area_chart_6(request):
    try:
        print("Fetching grouped supplier stats data from repository...")
        repository = SupplierRepository()
        queryset = repository.get_suppliers_with_product_count()
        data = queryset.values('supplier_id', 'name', 'total_products')
        print(f"Fetched data: {list(data)}")

        # Перетворення даних у DataFrame
        df = pd.DataFrame(list(data))
        if df.empty:
            print("No data available in DataFrame")
            return JsonResponse({"error": "No data available for area chart"}, status=404)

        # Отримання параметра фільтрації
        min_total_products = int(request.GET.get('min_total_products', 0))
        print(f"Minimum total products filter: {min_total_products}")

        # Застосування фільтрації
        df = df[df['total_products'] >= min_total_products]

        if df.empty:
            print("Filtered DataFrame is empty")
            return JsonResponse({"error": "No data matches the filter."}, status=404)

        # Групування по кількості продуктів
        product_group = df.groupby('total_products').agg(
            total_suppliers=('supplier_id', 'count'),
            average_products=('total_products', 'mean')
        ).reset_index()

        product_group = product_group.sort_values(by='total_suppliers', ascending=False)

        # Перетворення total_products у float для сумісності
        product_group['total_products'] = product_group['total_products'].astype(float)
        product_group['total_suppliers'] = product_group['total_suppliers'].astype(float)

        # Створення графіка області
        print("Creating area chart...")
        p = figure(
            height=500, width=800,
            title="Suppliers Distribution by Total Products",
            toolbar_location=None,
            tools="hover",
            tooltips="@total_products: @total_suppliers Suppliers"
        )

        # Додавання області
        p.varea(
            x=product_group['total_products'],
            y1=0,
            y2=product_group['total_suppliers'],
            fill_color="blue",
            fill_alpha=0.5,
        )

        # Додавання лінії
        p.line(
            x=product_group['total_products'],
            y=product_group['total_suppliers'],
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
        print(f"Error in bokeh_area_chart_suppliers: {e}")
        return JsonResponse({"error": str(e)}, status=500)
