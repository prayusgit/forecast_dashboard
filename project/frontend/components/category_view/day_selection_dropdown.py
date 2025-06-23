# Default Imports
from dash import dcc, html
import dash_bootstrap_components as dbc


day_selection_dropdown = html.Div([
                            html.Label("Select Forecast Day:", style={'margin-bottom': '4px'}),
                            dcc.Dropdown(
                                    id='forecast-dropdown',
                                    options=[
                                        {"label": "1 Day After", "value": "1 Day"},
                                        {"label": "2 Days After", "value": "2 Days"},
                                        {"label": "3 Days After", "value": "3 Days"},
                                    ],
                                    value="1 Day",
                                    clearable=False,
                                )
                            ], className='m-1')