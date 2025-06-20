import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Sample mapping
category_to_products = {
    "Topup": ["NTC Topup", "Ncell Topup"],
    "Banking": ["P2P Transfer", "Bank Withdrawal"],
}

# Simulate a dataset
def generate_sample_timeseries(product):
    today = pd.Timestamp.today().normalize()
    past_days = pd.date_range(today - pd.Timedelta(days=29), today - pd.Timedelta(days=1))
    future_days = pd.date_range(today, today + pd.Timedelta(days=6))

    past_values = np.random.randint(5000, 10000, len(past_days))
    future_values = past_values[-1] + np.cumsum(np.random.randint(-500, 500, len(future_days)))

    df_past = pd.DataFrame({"Date": past_days, "Amount": past_values, "Type": "Actual"})
    df_future = pd.DataFrame({"Date": future_days, "Amount": future_values, "Type": "Forecast"})

    df = pd.concat([df_past, df_future])
    df["Product"] = product
    return df


# Build Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H4("Product Forecast Line Chart", className="mt-4"),

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
            html.Label("Product(s):"),
            dcc.Dropdown(id="product-dropdown")
        ], width=6)
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="product-line-chart")
        ])
    ])
], fluid=True)


@app.callback(
    Output("product-dropdown", "options"),
    Output("product-dropdown", "value"),
    Input("category-dropdown", "value")
)
def update_products(category):
    if category:
        products = category_to_products[category]
        return [{"label": p, "value": p} for p in products], products
    return [], []


@app.callback(
    Output("product-line-chart", "figure"),
    Input("product-dropdown", "value")
)
def update_line_chart(product):
    if not product:
        return px.line(title="No product selected")

    df = generate_sample_timeseries(product)

    fig = px.line(
        df,
        x="Date",
        y="Amount",
        color="Product",
        line_dash="Type",
        markers=True,
        title=f"{product} - Past 30 Days + Next 7 Days Forecast"
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Transaction Amount (NPR)",
        hovermode="x unified"
    )
    return fig


if __name__ == '__main__':
    app.run(debug=True)
