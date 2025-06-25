# Default Imports
import dash_bootstrap_components as dbc
from dash import html

# Module Imports
from components.category_view.prediction_barchart import amount_barchart, volume_barchart
from components.category_view.day_selection_dropdown import day_selection_dropdown
from components.category_view.multi_category_selection_dropdown import multi_category_selection_dropdown
from components.category_view.kpi_section import kpi_section

def transaction_forecast_layout():
    return dbc.Card([
            dbc.CardHeader('Day to Day Transaction Forecast'),

            dbc.CardBody([
                html.H4("📊 Transaction Amount and Volume Forecast", className='mb-4'),
                dbc.Row([
                    dbc.Col(multi_category_selection_dropdown, width=6),
                    dbc.Col(width=2),
                    dbc.Col(day_selection_dropdown, width=4)
                ]),
                kpi_section,
                dbc.Row([
                    dbc.Col(amount_barchart, className='col-6'),
                    dbc.Col(volume_barchart, className='col-6'),
                ])
            ])
        ], className='mb-4')