# Default Imports
from dash import Output, Input
import plotly.express as px
import pandas as pd
import requests


def register_product_comparison_callback(app):
    @app.callback(
        Output("product-comparison-barchart", "figure"),
        Input("product-view-category-dropdown", "value"),
        Input("multi-product-selection-multi-dropdown", "value")
    )
    def update_bar_chart(category, selected_products):
        if not selected_products:
            return px.bar(title="No products selected")

        response = requests.post('http://127.0.0.1:8000/api/product/forecast', json={
                                                                                    'category': category,
                                                                                    'products': selected_products}).json()
        df = pd.DataFrame(response['data'])

        fig = px.bar(
            df.sort_values("transaction_amount"),
            x="transaction_amount",
            y="product",
            orientation="h",
            color="product",
            text="transaction_amount",
            title="Predicted Transaction Amount for Next 7 Days"
        )

        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(
            xaxis_title="Total Predicted Amount (NPR)",
            yaxis_title="product",
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
        response = requests.get(f'http://127.0.0.1:8000/api/info/category_to_products/{category}').json()
        products = response['products']
        options = [{"label": p, "value": p} for p in products]

        default_choice = products[:5]
        if product not in default_choice:
            default_choice.append(product)
        return options, default_choice  # Preselect all by default


