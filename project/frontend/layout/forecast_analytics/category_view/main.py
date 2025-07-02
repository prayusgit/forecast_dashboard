import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output

# Module Imports
from .transaction_forecast_card import transaction_forecast_layout
from .amount_growth_analytics_card import amount_growth_analytics_layout
from .volume_growth_analytics_card import volume_growth_analytics_layout
from .wow_growth_summary_card import wow_growth_summary_layout
from .alert_card import alert_notification_layout
from components.category_view.category_email_section import category_email_section

def create_category_view_layout():
    return html.Div([
            transaction_forecast_layout(),
            dbc.Row([
                dbc.Col(amount_growth_analytics_layout(), width=7),
                dbc.Col(wow_growth_summary_layout(), width=5)
            ], className='mb-4'),
            dbc.Row([
                dbc.Col(volume_growth_analytics_layout(), width=7),
                dbc.Col(alert_notification_layout(), width=5)
            ], className='mb-4'),

            dbc.Row([
                dbc.Col('', width=7),
                dbc.Col(category_email_section, width=5)
            ], className='mb-4'),

        ])

