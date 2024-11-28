import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pharmacyApp.models import Product
from pharmacyApp.plotly_charts import generate_performance_charts

# Константи
BATCH_SIZES = [10, 50, 200, 500, 1000]
WORKER_COUNTS = [1, 2, 10, 50, 61]


# Запит JOIN через Django ORM
def perform_join_query():
    return list(
        Product.objects.select_related('supplier')
        .values('name', 'supplier__name')
    )


# Обгортка для запуску запитів
def perform_queries_in_batch(batch_size):
    for _ in range(batch_size):
        perform_join_query()


# Виконання запитів
def execute_queries_in_threads_or_processes(query_function, batch_size, workers, method):
    start_time = time.time()

    if method == "threads":
        with ThreadPoolExecutor(max_workers=workers) as executor:
            executor.map(query_function, [batch_size] * workers)
    elif method == "processes":
        with ProcessPoolExecutor(max_workers=workers) as executor:
            executor.map(query_function, [batch_size] * workers)
    else:
        raise ValueError("Invalid method. Use 'threads' or 'processes'.")

    end_time = time.time()
    return end_time - start_time


# Тестування
def test_performance():
    results = []
    for batch_size in BATCH_SIZES:
        for workers in WORKER_COUNTS:
            for method in ["threads", "processes"]:
                execution_time = execute_queries_in_threads_or_processes(
                    perform_queries_in_batch, batch_size, workers, method
                )
                results.append(
                    {
                        "batch_size": batch_size,
                        "workers": workers,
                        "method": method,
                        "time": execution_time,
                    }
                )

    # Генерація графіків
    charts = generate_performance_charts(results)
    return charts
