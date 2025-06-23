# Default Imports
from dash import dcc, html

# Sample options (e.g., service categories)
categories = ['NTC Topup', 'Bank Withdrawal', 'Electricity Bill', 'P2P Transfer', 'Insurance Premium']

multi_category_selection_dropdown = html.Div([
                                        html.Label("Select Categories:", style={'margin-bottom': '4px'}),
                                        dcc.Dropdown(
                                            id='multi-category-selection-dropdown',
                                            multi=True,
                                            placeholder="Select one or more categories...",
                                            style={'width': '100%'}
                                        )
                                    ], className='m-1')

wow_multi_category_selection_dropdown = html.Div([
                                        html.Label("Select Categories:", style={'margin-bottom': '4px'}),
                                        dcc.Dropdown(
                                            id='wow-multi-category-selection-dropdown',
                                            multi=True,
                                            placeholder="Select one or more categories...",
                                            style={'width': '100%'}
                                        )
                                    ], className='mb-3')
