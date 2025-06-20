# Default Imports
import pandas as pd
import plotly.express as px
from dash import Input, Output

forecast_data = {
    "1 Day": [
        {"Service": "NTC Topup", "Transactions": 12500, "Amount": 8750000},
        {"Service": "Bank Withdrawal", "Transactions": 8200, "Amount": 45600000},
        {"Service": "Electricity Bill", "Transactions": 15800, "Amount": 12300000},
        {"Service": "P2P Transfer", "Transactions": 22000, "Amount": 67800000},
        {"Service": "Insurance Premium", "Transactions": 450, "Amount": 2100000},
    ],
    "2 Days": [
        {"Service": "NTC Topup", "Transactions": 26000, "Amount": 18000000},
        {"Service": "Bank Withdrawal", "Transactions": 16800, "Amount": 89000000},
        {"Service": "Electricity Bill", "Transactions": 31000, "Amount": 26000000},
        {"Service": "P2P Transfer", "Transactions": 44000, "Amount": 135000000},
        {"Service": "Insurance Premium", "Transactions": 920, "Amount": 4250000},
    ],
    "3 Days": [
        {"Service": "NTC Topup", "Transactions": 39000, "Amount": 27500000},
        {"Service": "Bank Withdrawal", "Transactions": 24800, "Amount": 134000000},
        {"Service": "Electricity Bill", "Transactions": 47000, "Amount": 39500000},
        {"Service": "P2P Transfer", "Transactions": 66000, "Amount": 200000000},
        {"Service": "Insurance Premium", "Transactions": 1400, "Amount": 6300000},
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

