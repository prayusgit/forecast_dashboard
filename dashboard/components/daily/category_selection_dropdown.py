# Default imports
import dash_bootstrap_components as dbc
from dash import dcc, html
from datetime import datetime, timedelta
import numpy as np


# Sample data generation
categories = ['NTC Topup', 'Bank Withdrawal', 'Electricity Bill', 'P2P Transfer', 'Insurance Premium']


amount_category_selection_dropdown = dbc.Row([
        dbc.Col(html.H4("📈 Revenue Growth Analytics"), width=8),
        dbc.Col([
            html.Label("Select Category:", style={'margin-bottom': '4px'}),
            dcc.Dropdown(
                id='amount-category-selection-dropdown',
                options=[{'label': cat, 'value': cat} for cat in categories],
                value='NTC Topup',
                clearable=False,
                )], width=4)
            ], className="my-3")


volume_category_selection_dropdown = dbc.Row([
        dbc.Col(html.H4("📈 Traffic Flow Analytics"), width=8),
        dbc.Col([
            html.Label("Select Category:", style={'margin-bottom': '4px'}),
            dcc.Dropdown(
                id='volume-category-selection-dropdown',
                options=[{'label': cat, 'value': cat} for cat in categories],
                value='NTC Topup',
                clearable=False,
                )], width=4)
            ], className="my-3")

