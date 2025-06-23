# Default Imports
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import pandas as pd
from datetime import datetime, timedelta

# Module Imports
from components.category_view.multi_category_selection_dropdown import wow_multi_category_selection_dropdown

def wow_growth_summary_layout():
    return dbc.Card([
            dbc.CardHeader('Week-over-Week (WoW) Growth Summary'),
            dbc.CardBody([
                html.H4("WoW Forecast Summary", className="text-center ma-2 mb-3"),
                wow_multi_category_selection_dropdown,
                html.Div(id='wow-growth-table')
            ])
        ])