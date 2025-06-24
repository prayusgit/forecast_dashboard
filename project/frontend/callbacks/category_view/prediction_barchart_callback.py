# Default Imports
import pandas as pd
import plotly.express as px
from dash import Input, Output
import requests
import re

forecast_data = {
    "1 Day": [
        {"Service": "bank_transaction", "Transactions": 12500, "Amount": 8750000},
        {"Service": "bill_payment", "Transactions": 8200, "Amount": 45600000},
        {"Service": "education", "Transactions": 15800, "Amount": 12300000},
        {"Service": "entertainment", "Transactions": 22000, "Amount": 67800000},
        {"Service": "government", "Transactions": 450, "Amount": 2100000},
        {"Service": "insurance", "Transactions": 560, "Amount": 3450000},
        {"Service": "loan", "Transactions": 1300, "Amount": 15000000},
        {"Service": "shopping", "Transactions": 8900, "Amount": 7200000},
        {"Service": "topup", "Transactions": 16800, "Amount": 9500000},
    ],
    "2 Days": [
        {"Service": "bank_transaction", "Transactions": 26000, "Amount": 18000000},
        {"Service": "bill_payment", "Transactions": 16800, "Amount": 89000000},
        {"Service": "education", "Transactions": 31000, "Amount": 26000000},
        {"Service": "entertainment", "Transactions": 44000, "Amount": 135000000},
        {"Service": "government", "Transactions": 920, "Amount": 4250000},
        {"Service": "insurance", "Transactions": 1120, "Amount": 6800000},
        {"Service": "loan", "Transactions": 2600, "Amount": 32000000},
        {"Service": "shopping", "Transactions": 17800, "Amount": 14500000},
        {"Service": "topup", "Transactions": 33600, "Amount": 19000000},
    ],
    "3 Days": [
        {"Service": "bank_transaction", "Transactions": 39000, "Amount": 27500000},
        {"Service": "bill_payment", "Transactions": 24800, "Amount": 134000000},
        {"Service": "education", "Transactions": 47000, "Amount": 39500000},
        {"Service": "entertainment", "Transactions": 66000, "Amount": 200000000},
        {"Service": "government", "Transactions": 1400, "Amount": 6300000},
        {"Service": "insurance", "Transactions": 1680, "Amount": 10200000},
        {"Service": "loan", "Transactions": 3900, "Amount": 48000000},
        {"Service": "shopping", "Transactions": 26700, "Amount": 21700000},
        {"Service": "topup", "Transactions": 50400, "Amount": 28500000},
    ]
}


def get_forecast_df(days):
    return pd.DataFrame(forecast_data[days])

def register_prediction_callback(app):
    @app.callback(
        Output('amount-forecast-graph', 'figure'),
        [Input('multi-category-selection-dropdown', 'value'),
         Input('forecast-dropdown', 'value')]
    )
    def update_amount_barchart(selected_categories, selected_forecast_day):

        df = get_forecast_df(selected_forecast_day)
        df = df[df['Service'].isin(selected_categories)]
        fig = px.bar(
            df,
            x='Service',
            y='Amount',
            text='Amount',
            title=f"Transaction Amount Forecast - {selected_forecast_day}",
            labels={"Transactions": "Predicted Transactions Amount"},
            color='Service'
        )
        fig.update_traces(texttemplate='%{text:,}', textposition='outside',showlegend=False)
        fig.update_layout(yaxis_title='Transaction Amount (Rupees)', xaxis_title='Service Category')
        return fig

    @app.callback(
        Output('volume-forecast-graph', 'figure'),
        [Input('multi-category-selection-dropdown', 'value'),
         Input('forecast-dropdown', 'value')]
    )
    def update_volume_barchart(selected_categories, selected_forecast_day):
        df = get_forecast_df(selected_forecast_day)
        df = df[df['Service'].isin(selected_categories)]
        fig = px.bar(
            df,
            x='Service',
            y='Transactions',
            text='Transactions',
            title=f"  ",
            labels={"Transactions": "Predicted Transactions Volume"},
            color='Service'
        )
        fig.update_traces(texttemplate='%{text:,}', textposition='outside', showlegend=False)
        fig.update_layout(yaxis_title='Number of Transactions', xaxis_title='Service Category')
        return fig

    @app.callback(
        Output('multi-category-selection-dropdown', 'options'),
        Output('multi-category-selection-dropdown', 'value'),
        Input('multi-category-selection-dropdown', 'id')
    )
    def update_multi_dropdown(_):
        categories = requests.get('http://127.0.0.1:8000/api/info/categories').json()['categories']
        options = [{'label': cat, 'value': cat} for cat in categories]
        return options, categories[:7]

