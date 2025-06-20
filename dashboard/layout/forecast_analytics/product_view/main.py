# Default Imports
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output


# Module Imports
from .product_forecast_card import product_forecast_layout

def create_product_view_layout():
    return html.Div([
            product_forecast_layout(),
        ])

