# Default imports
import dash_bootstrap_components as dbc
from dash import dcc, html
from datetime import datetime, timedelta
import numpy as np


# Sample data generation
categories = ['NTC Topup', 'Bank Withdrawal', 'Electricity Bill', 'P2P Transfer', 'Insurance Premium']


amount_category_selection_dropdown = html.Div([
            html.Label("Select Category:", style={'margin-bottom': '4px'}),
            dcc.Dropdown(
                id='amount-category-selection-dropdown',
                options=[{'label': cat, 'value': cat} for cat in categories],
                value='NTC Topup',
                clearable=False,
                )
            ])


volume_category_selection_dropdown = html.Div([
            html.Label("Select Category:", style={'margin-bottom': '4px'}),
            dcc.Dropdown(
                id='volume-category-selection-dropdown',
                options=[{'label': cat, 'value': cat} for cat in categories],
                value='NTC Topup',
                clearable=False,
                )
            ])

