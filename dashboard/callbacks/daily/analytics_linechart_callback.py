# Default Imports
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta


# Sample data generation
categories = ['NTC Topup', 'Bank Withdrawal', 'Electricity Bill', 'P2P Transfer', 'Insurance Premium']
today = datetime.today().date()
days = 30

np.random.seed(42)
historical_data = {
    cat: [np.random.randint(5000, 15000) + i*50 + np.random.randint(-200, 200) for i in range(days)]
    for cat in categories
}
forecast_data = {
    cat: [historical_data[cat][-1] + (i+1)*100 + np.random.randint(-150, 150) for i in range(5)]
    for cat in categories
}
dates_past = [today - timedelta(days=days - i) for i in range(days)]
dates_future = [today + timedelta(days=i+1) for i in range(5)]


def register_analytics_callback(app):
    @app.callback(
        Output('amount-growth-linechart', 'figure'),
        Input('amount-category-selection-dropdown', 'value')
    )
    def update_amount_growth_linechart(category):
        fig = go.Figure()

        # Plot historical data
        fig.add_trace(go.Scatter(
            x=dates_past,
            y=historical_data[category],
            mode='lines+markers',
            name='Actual',
            line=dict(color='blue')
        ))

        # Plot forecast data
        fig.add_trace(go.Scatter(
            x=dates_future,
            y=forecast_data[category],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='green', dash='dash')
        ))

        fig.update_layout(
            title=f"{category} – Last 30 Days + Forecast",
            xaxis_title="Date",
            yaxis_title="Transactions Amount (Rupees)",
            template="plotly_white",
            hovermode='x unified'
        )
        return fig

    @app.callback(
        Output('volume-growth-linechart', 'figure'),
        Input('volume-category-selection-dropdown', 'value')
    )
    def update_volume_growth_linechart(category):
        fig = go.Figure()

        # Plot historical data
        fig.add_trace(go.Scatter(
            x=dates_past,
            y=historical_data[category],
            mode='lines+markers',
            name='Actual',
            line=dict(color='blue')
        ))

        # Plot forecast data
        fig.add_trace(go.Scatter(
            x=dates_future,
            y=forecast_data[category],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='green', dash='dash')
        ))

        fig.update_layout(
            title=f"  ",
            xaxis_title="Date",
            yaxis_title="Number of Transactions",
            template="plotly_white",
            hovermode='x unified'
        )
        return fig
