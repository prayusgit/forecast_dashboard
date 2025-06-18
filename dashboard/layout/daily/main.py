import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output

# Module Imports
from .transaction_forecast_card import transaction_forecast_layout
from .growth_analytics_card import  growth_analytics_layout

def create_daily_layout():
    return html.Div([
            transaction_forecast_layout(),
            growth_analytics_layout()
        ])

