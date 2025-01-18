import plotly.express as px
import plotly.io as pio
import pandas as pd

def generate_performance_charts(results):
    charts = []
    df = pd.DataFrame(results)

    # Генеруємо графіки для кожної комбінації batch_size і method
    for (batch_size, method), group in df.groupby(["batch_size", "method"]):
        fig = px.line(
            group,
            x="workers",
            y="time",
            title=f"Batch Size: {batch_size}, Method: {method.capitalize()}",
            labels={"workers": "Number of Workers", "time": "Execution Time (s)"},
            markers=True,
        )
        charts.append({"batch_size": batch_size, "method": method, "chart": pio.to_json(fig)})

    return charts
