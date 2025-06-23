# Default Imports
import dash_bootstrap_components as dbc
from dash import html, dcc

# Module Imports
from components.category_view.growth_analytics_linechart import  volume_growth_linechart
from components.category_view.category_selection_dropdown import volume_category_selection_dropdown

def volume_growth_analytics_layout():
    return dbc.Card([
            dbc.CardHeader('Request Traffic Analytics'),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(html.H4("📈 Traffic Flow Analytics"), width=8),
                    dbc.Col(volume_category_selection_dropdown, width=4)
                ]),
                volume_growth_linechart
            ])
        ])

