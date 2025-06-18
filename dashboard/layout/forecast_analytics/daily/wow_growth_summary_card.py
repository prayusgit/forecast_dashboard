# Default Imports
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import pandas as pd
from datetime import datetime, timedelta

# Module Imports


def wow_growth_summary_layout():
    return dbc.Card([
            dbc.CardHeader('WoW Growth Summary'),
            dbc.CardBody([
                html.H4("Week-over-Week (WoW) Forecast Summary", className="text-center my-4"),
                html.Div(id='wow-growth-table')
            ])
        ])