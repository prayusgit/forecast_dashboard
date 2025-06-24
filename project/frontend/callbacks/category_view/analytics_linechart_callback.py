# Default Imports
from dash import dcc, html, Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests


def register_analytics_callback(app):
    @app.callback(
        Output("amount-growth-linechart", "figure"),
        Input("amount-category-selection-dropdown", "value")
    )
    def update_amount_growth_linechart(category):
        if not category:
            return go.Figure()

        response = requests.get(f'http://127.0.0.1:8000/api/category/forecast/category-amount/{category}').json()

        df_past, df_future = pd.DataFrame(response['past_data'], ), pd.DataFrame(response['future_data'])

        df_past['transaction_date'] = pd.to_datetime(df_past['transaction_date'])
        df_future['transaction_date'] = pd.to_datetime(df_future['transaction_date'])


        fig = go.Figure()

        # Actual Line
        fig.add_trace(go.Scatter(
            x=df_past["transaction_date"], y=df_past["transaction_amount"],
            mode="lines+markers",
            name="Actual",
            line=dict(color="blue")
        ))

        # Forecast Line
        fig.add_trace(go.Scatter(
            x=df_future["transaction_date"], y=df_future["transaction_amount"],
            mode="lines+markers",
            name="Forecast",
            line=dict(color="green", dash="dash")
        ))

        # Confidence Interval: Shaded region
        fig.add_trace(go.Scatter(
            x=pd.concat([df_future["transaction_date"], df_future["transaction_date"][::-1]]),
            y=pd.concat([df_future["upper"], df_future["lower"][::-1]]),
            fill='toself',
            fillcolor='rgba(0, 200, 0, 0.1)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            name="Confidence Interval",
            showlegend=True
        ))

        fig.update_layout(
            title=f"{category} —  Past 30 days + 7 days Forecast",
            xaxis_title="Date",
            yaxis_title="Transaction Amount (NPR)",
            hovermode="x unified",
            template ="plotly_white",
        )

        return fig

    @app.callback(
        Output("volume-growth-linechart", "figure"),
        Input("volume-category-selection-dropdown", "value")
    )
    def update_volume_growth_linechart(category):
        if not category:
            return go.Figure()

        response = requests.get(f'http://127.0.0.1:8000/api/category/forecast/category-count/{category}').json()

        df_past, df_future = pd.DataFrame(response['past_data'], ), pd.DataFrame(response['future_data'])

        df_past['transaction_date'] = pd.to_datetime(df_past['transaction_date'])
        df_future['transaction_date'] = pd.to_datetime(df_future['transaction_date'])

        fig = go.Figure()

        # Actual Line
        fig.add_trace(go.Scatter(
            x=df_past["transaction_date"], y=df_past["transaction_count"],
            mode="lines+markers",
            name="Actual",
            line=dict(color="blue")
        ))

        # Forecast Line
        fig.add_trace(go.Scatter(
            x=df_future["transaction_date"], y=df_future["transaction_count"],
            mode="lines+markers",
            name="Forecast",
            line=dict(color="green", dash="dash")
        ))

        # Confidence Interval: Shaded region
        fig.add_trace(go.Scatter(
            x=pd.concat([df_future["transaction_date"], df_future["transaction_date"][::-1]]),
            y=pd.concat([df_future["upper"], df_future["lower"][::-1]]),
            fill='toself',
            fillcolor='rgba(0, 200, 0, 0.1)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            name="Confidence Interval",
            showlegend=True
        ))

        fig.update_layout(
            title=f"{category} —  Past 30 days + 7 days Forecast",
            xaxis_title="Date",
            yaxis_title="Number of Transaction",
            hovermode="x unified",
            template="plotly_white",
        )
        return fig

    @app.callback(
        Output('amount-category-selection-dropdown', 'options'),
        Output('amount-category-selection-dropdown', 'value'),
        Input('amount-category-selection-dropdown', 'id')
    )
    def update_amount_category_dropdown(_):
        categories = requests.get('http://127.0.0.1:8000/api/info/categories').json()['categories']
        options = [{'label': cat, 'value': cat} for cat in categories]
        return options, categories[0]

    @app.callback(
        Output('volume-category-selection-dropdown', 'options'),
        Output('volume-category-selection-dropdown', 'value'),
        Input('volume-category-selection-dropdown', 'id')
    )
    def update_volume_category_dropdown(_):
        categories = requests.get('http://127.0.0.1:8000/api/info/categories').json()['categories']
        options = [{'label': cat, 'value': cat} for cat in categories]
        return options, categories[0]

