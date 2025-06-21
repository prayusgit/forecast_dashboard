# Default Imports
from dash import Input, Output, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


category_to_products = {
    "Topup": ["NTC Topup", "Ncell Topup"],
    "Bill Payment": ["Electricity Bill", "Khanepani Bill", "TV Recharge"],
    "Banking": ["P2P Transfer", "Bank Withdrawal"],
    "Insurance": ["Insurance Premium"]
}


def generate_sample_timeseries_with_ci(product):
    today = pd.Timestamp.today().normalize()
    past_days = pd.date_range(today - pd.Timedelta(days=29), today - pd.Timedelta(days=1))
    future_days = pd.date_range(today, today + pd.Timedelta(days=6))

    past_values = np.random.randint(5000, 10000, len(past_days))
    forecast_base = past_values[-1]
    forecast_values = forecast_base + np.cumsum(np.random.randint(-500, 500, len(future_days)))

    # Confidence intervals: ±10%
    lower_bound = forecast_values * 0.90
    upper_bound = forecast_values * 1.10

    df_past = pd.DataFrame({
        "Date": past_days,
        "Amount": past_values,
        "Type": "Actual"
    })

    df_future = pd.DataFrame({
        "Date": future_days,
        "Amount": forecast_values,
        "Lower": lower_bound,
        "Upper": upper_bound,
        "Type": "Forecast"
    })

    df_past["Product"] = product
    df_future["Product"] = product

    return df_past, df_future

def register_growth_linechart_callback(app):
    @app.callback(
        Output("product-amount-growth-linechart", "figure"),
        Input("product-view-product-dropdown", "value")
    )
    def update_line_chart(product):
        if not product:
            return go.Figure()

        df_past, df_future = generate_sample_timeseries_with_ci(product)

        fig = go.Figure()

        # Actual Line
        fig.add_trace(go.Scatter(
            x=df_past["Date"], y=df_past["Amount"],
            mode="lines+markers",
            name="Actual",
            line=dict(color="blue")
        ))

        # Forecast Line
        fig.add_trace(go.Scatter(
            x=df_future["Date"], y=df_future["Amount"],
            mode="lines+markers",
            name="Forecast",
            line=dict(color="green", dash="dash")
        ))

        # Confidence Interval: Shaded region
        fig.add_trace(go.Scatter(
            x=pd.concat([df_future["Date"], df_future["Date"][::-1]]),
            y=pd.concat([df_future["Upper"], df_future["Lower"][::-1]]),
            fill='toself',
            fillcolor='rgba(0, 200, 0, 0.1)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            name="Confidence Interval",
            showlegend=True
        ))

        fig.update_layout(
            title=f"{product} — Forecast with Confidence Interval",
            xaxis_title="Date",
            yaxis_title="Transaction Amount (NPR)",
            hovermode="x unified",
            template="plotly_white"

        )

        return fig

    @app.callback(
        Output("product-view-product-dropdown", "options"),
        Output("product-view-product-dropdown", "value"),
        Input("product-view-category-dropdown", "value")
    )
    def update_product_dropdown(category):
        if category:
            products = category_to_products[category]
            options = [{"label": p, "value": p} for p in products]
            return options, products[0]  # pre-select all products by default
        return [], []
