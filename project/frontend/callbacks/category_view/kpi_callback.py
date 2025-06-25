# Default Imports
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input
from datetime import datetime, timedelta
import requests

# Module Imports
from utils.helper_functions import format

def register_kpi_callback(app):
    @app.callback(
        Output('kpi-category-transaction-amount', 'children'),
        Output('kpi-category-transaction-count', 'children'),
        Output('kpi-day-label-1', 'children'),
        Output('kpi-day-label-2', 'children'),
        Input('category-data-store', 'data')
    )
    def update_kpi_count(data):
        selected_forecast_day = data['selected_forecast_day']
        data = data['data']

        transaction_amount = "NPR " + format(sum(data['transaction_amount'].values()))
        transaction_count = format(sum(data['transaction_count'].values()))

        label = f' ({selected_forecast_day})'
        return transaction_amount, transaction_count, label, label
