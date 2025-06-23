# Default Imports
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output


# Module Imports
from .product_forecast_card import product_forecast_layout
from .product_comparison_card import product_comparison_layout
def create_product_view_layout():
    return html.Div([
            html.Div(product_forecast_layout(), className='mb-4'),
            html.Div(product_comparison_layout(), className='mb-4')
        ])

