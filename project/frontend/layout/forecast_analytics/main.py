from dash import dcc, html
import dash_bootstrap_components as dbc

# Module Imports
from components.category_view.category_data_store import category_data_store, wow_table_data_store
from components.product_view.product_data_store import product_data_store

def create_forecast_analytics_layout():
    return dbc.Container([
            html.H2("Forecast and Analytics Dashboard", className="text-center my-4"),

            dbc.Tabs(id="forecast-tabs", active_tab='category-view', children=[
                dbc.Tab(label='Category View', tab_id='category-view'),
                dbc.Tab(label='Product View', tab_id='product-view'),
            ], className="mb-4"),

            # dbc.Card([
            #     dbc.CardHeader('Daily Forecast'),
            #     dbc.CardBody(id='tabs-content')
            # ], className="shadow-sm"),

            html.Div(id='tabs-content'),
            category_data_store,
            wow_table_data_store,
            product_data_store,
    ])