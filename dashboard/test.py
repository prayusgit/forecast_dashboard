import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np

# Category → Products map
category_to_products = {
    "Topup": ["NTC Topup", "Ncell Topup"],
    "Banking": ["P2P Transfer", "Bank Withdrawal"],
    "Bills": ["Electricity", "TV Recharge", "Khanepani"]
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


# Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H4("Next Week Product Comparison", className="mt-4"),

    dbc.Row([
        dbc.Col([
            html.Label("Category:"),
            dcc.Dropdown(
                id="category-dropdown",
                options=[{"label": c, "value": c} for c in category_to_products],
                value="Topup",
                clearable=False
            )
        ], width=4),

        dbc.Col([
            html.Label("Select Products to Compare:"),
            dcc.Dropdown(
                id="product-multi-dropdown",
                multi=True,
                placeholder="Choose products to compare"
            )
        ], width=8),
    ]),

    html.Br(),

    dcc.Graph(id="weekly-comparison-bar-chart")
], fluid=True)


@app.callback(
    Output("product-multi-dropdown", "options"),
    Output("product-multi-dropdown", "value"),
    Input("category-dropdown", "value")
)
def update_products(category):
    if not category:
        return [], []
    products = category_to_products[category]
    options = [{"label": p, "value": p} for p in products]
    return options, products  # Preselect all by default


@app.callback(
    Output("weekly-comparison-bar-chart", "figure"),
    Input("category-dropdown", "value"),
    Input("product-multi-dropdown", "value")
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


if __name__ == "__main__":
    app.run(debug=True)
