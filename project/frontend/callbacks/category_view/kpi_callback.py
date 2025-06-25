# Default Imports
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input
from datetime import datetime, timedelta
import requests


def format(amount):
    if amount >= 10_000_000:
        return f"{amount / 1_00_00_000:.2f} Cr"
    elif amount >= 1_00_000:
        return f"{amount / 1_00_000:.2f} Lakh"
    elif amount >= 1_000:
        return f"{amount / 1_000:.2f} Thousand"
    else:
        return f"{amount:.2f}"


def register_kpi_callback(app):
    @app.callback(
        Output('kpi-category-transaction-amount', 'children'),
        Output('kpi-category-transaction-count', 'children'),
        Input('data-store', 'data')
    )
    def update_kpi_count(data):
        data = data['data']

        transaction_amount = "NPR " + format(sum(data['transaction_amount'].values()))
        transaction_count = format(sum(data['transaction_count'].values()))

        return transaction_amount, transaction_count
