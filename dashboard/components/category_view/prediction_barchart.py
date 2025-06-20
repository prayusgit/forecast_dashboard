import dash
import dash_bootstrap_components as dbc
from dash import html, dcc


amount_barchart = html.Div([
    dcc.Graph(id='amount-forecast-graph')
])

volume_barchart = html.Div([
    dcc.Graph(id='volume-forecast-graph')
])