# Default Imports
import dash_bootstrap_components as dbc


# Module Imports
from components.daily.prediction_barchart import amount_barchart, volume_barchart
from components.daily.day_selection_dropdown import day_selection_dropdown
from components.daily.kpi_section import kpi_section

def transaction_forecast_layout():
    return dbc.Card([
            dbc.CardHeader('Day to Day Transaction Forecast'),
            dbc.CardBody([
                day_selection_dropdown,
                kpi_section,
                dbc.Row([
                    dbc.Col(amount_barchart, className='col-6'),
                    dbc.Col(volume_barchart, className='col-6'),
                ])
            ])
        ], className='mb-4')