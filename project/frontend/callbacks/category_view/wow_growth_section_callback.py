# Default imports
import pandas as pd
from datetime import datetime, timedelta
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import requests


# --- Callback with no inputs: triggered automatically on load
def register_dash_table_callback(app):
    @app.callback(
        Output("wow-growth-table", "children"),
        Input('wow-multi-category-selection-dropdown', 'value')
    )
    def display_growth_table(categories):
        response = requests.post('http://127.0.0.1:8000/api/category/wow-growth', json={'req_categories':categories}).json()['wow_growth_list']

        df = pd.DataFrame(response, columns=["Category", "Week Forecast (Rs)", "WoW Growth (%)"])

        return dash_table.DataTable(
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict("records"),
            style_cell={
                'textAlign': 'center',
                'padding': '10px',
                'font-family': 'Arial',
            },
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{WoW Growth (%)} > 0',
                        'column_id': 'WoW Growth (%)'
                    },
                    'color': 'green',
                    'fontWeight': 'bold'
                },
                {
                    'if': {
                        'filter_query': '{WoW Growth (%)} < 0',
                        'column_id': 'WoW Growth (%)'
                    },
                    'color': 'red',
                    'fontWeight': 'bold'
                },
            ],
            style_table={'overflowX': 'auto'},
            page_size=10
        )

    @app.callback(
        Output('wow-multi-category-selection-dropdown', 'options'),
        Output('wow-multi-category-selection-dropdown', 'value'),
        Input('wow-multi-category-selection-dropdown', 'id')
    )
    def update_multi_dropdown(_):
        categories = requests.get('http://127.0.0.1:8000/api/info/categories').json()['categories']
        options = [{'label': cat, 'value': cat} for cat in categories]
        return options, categories[:5]

