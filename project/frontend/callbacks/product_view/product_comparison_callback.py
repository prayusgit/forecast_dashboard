# Default Imports
from dash import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd


category_to_products = {
    "Topup": ["NTC Topup", "Ncell Topup"],
    "Bill Payment": ["Electricity Bill", "Khanepani Bill", "TV Recharge",'fdsafdas', 'fdsafdsafdsafd', 'fdsafdasffdas', 'fdsaf','fd'],
    "Banking": ["P2P Transfer", "Bank Withdrawal"],
    "Insurance": ["Insurance Premium"]
}

# Simulate forecast for next 7 days per product
def simulate_next_week_forecast(category):
    products = category_to_products[category]
    np.random.seed(42)
    forecast = []

    for prod in products:
        # 7 daily values
        daily_transactions = np.random.randint(500, 2000, 7)
        daily_amounts = np.random.randint(100_000, 700_000, 7)
        forecast.append({
            "Product": prod,
            "Predicted Transactions": daily_transactions.sum(),
            "Predicted Amount": daily_amounts.sum()
        })
    return pd.DataFrame(forecast)

def register_product_comparison_callback(app):
    @app.callback(
        Output("product-comparison-barchart", "figure"),
        Input("product-view-category-dropdown", "value"),
        Input("multi-product-selection-multi-dropdown", "value")
    )
    def update_bar_chart(category, selected_products):
        if not selected_products:
            return px.bar(title="No products selected")

        df = simulate_next_week_forecast(category)
        df = df[df["Product"].isin(selected_products)]

        fig = px.bar(
            df.sort_values("Predicted Amount"),
            x="Predicted Amount",
            y="Product",
            orientation="h",
            color="Product",
            text="Predicted Amount",
            title="Predicted Transaction Amount for Next 7 Days"
        )

        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(
            xaxis_title="Total Predicted Amount (NPR)",
            yaxis_title="Product",
            height=450
        )
        return fig

    @app.callback(
        Output("multi-product-selection-multi-dropdown", "options"),
        Output("multi-product-selection-multi-dropdown", "value"),
        Input("product-view-category-dropdown", "value"),
        Input("product-view-product-dropdown", "value")
    )
    def update_products(category, product):
        if not category:
            return [], []
        products = category_to_products[category]
        options = [{"label": p, "value": p} for p in products]

        default_choice = products[:5]
        if product not in default_choice:
            default_choice.append(product)
        return options, default_choice  # Preselect all by default


