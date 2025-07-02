# Default Imports
import pandas as pd
import plotly.express as px
from dash import Input, Output
import requests
import re


def register_prediction_callback(app):
    @app.callback(
        Output('amount-forecast-graph', 'figure'),
        Input('category-data-store', 'data')

    )
    def update_amount_barchart(data):
        df = pd.DataFrame(data['data'])

        selected_forecast_day = data['selected_forecast_day']
        fig = px.bar(
            df,
            x='category',
            y='transaction_amount',
            text='transaction_amount',
            title=f"Revenue Forecast - {selected_forecast_day}",
            labels={"transaction_amount": "Predicted Amount (Rs)"},
            color='category'
        )
        fig.update_traces(texttemplate='%{text:,}', textposition='outside',showlegend=False)
        fig.update_layout(yaxis_title='Transaction Amount (Rupees)', xaxis_title='Service Category')
        return fig

    @app.callback(
        Output('volume-forecast-graph', 'figure'),
        Input('category-data-store', 'data')
    )
    def update_volume_barchart(data):

        df = pd.DataFrame(data['data'])

        selected_forecast_day = data['selected_forecast_day']
        fig = px.bar(
                df,
                x='category',
                y='transaction_count',
                text='transaction_count',
                title=f"Number of Transactions Forecast - {selected_forecast_day}",
                labels={"transaction_count": "No. of Transactions"},
                color='category'
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

