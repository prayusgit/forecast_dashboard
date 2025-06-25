# Default Imports
from dash import dcc, html
import dash_bootstrap_components as dbc


day_selection_dropdown = html.Div([
                            html.Label("Select Forecast Day:", style={'margin-bottom': '4px'}),
                            dcc.Dropdown(
                                    id='forecast-dropdown',
                                    options=[
                                        {"label": "Today", "value": "Today"},
                                        {"label": "1 Day After", "value": "1 Day After"},
                                        {"label": "2 Days After", "value": "2 Days After"},
                                        {"label": "3 Days After", "value": "3 Days After"},
                                        {"label": "4 Days After", "value": "4 Days After"},
                                        {"label": "5 Days After", "value": "5 Days After"},
                                        {"label": "6 Days After", "value": "6 Days After"},
                                    ],
                                    value="Today",
                                    clearable=False,
                                )
                            ], className='m-1')