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
# today = datetime.today().date()
# days = 30
#
# np.random.seed(42)
# historical_data = {
#     cat: [np.random.randint(5000, 15000) + i*50 + np.random.randint(-200, 200) for i in range(days)]
#     for cat in categories
# }
# forecast_data = {
#     cat: [historical_data[cat][-1] + (i+1)*100 + np.random.randint(-150, 150) for i in range(5)]
#     for cat in categories
# }
# dates_past = [today - timedelta(days=days - i) for i in range(days)]
# dates_future = [today + timedelta(days=i+1) for i in range(5)]
#
#
# def register_analytics_callback(app):
#     @app.callback(
#         Output('amount-growth-linechart', 'figure'),
#         Input('amount-category-selection-dropdown', 'value')
#     )
#     def update_amount_growth_linechart(category):
#         fig = go.Figure()
#
#         # Plot historical data
#         fig.add_trace(go.Scatter(
#             x=dates_past,
#             y=historical_data[category],
#             mode='lines+markers',
#             name='Actual',
#             line=dict(color='blue')
#         ))
#
#         # Plot forecast data
#         fig.add_trace(go.Scatter(
#             x=dates_future,
#             y=forecast_data[category],
#             mode='lines+markers',
#             name='Forecast',
#             line=dict(color='green', dash='dash')
#         ))
#
#         fig.update_layout(
#             title=f"{category} – Last 30 Days + Forecast",
#             xaxis_title="Date",
#             yaxis_title="Transactions Amount (Rupees)",
#             template="plotly_white",
#             hovermode='x unified'
#         )
#         return fig
#
#     @app.callback(
#         Output('volume-growth-linechart', 'figure'),
#         Input('volume-category-selection-dropdown', 'value')
#     )
#     def update_volume_growth_linechart(category):
#         fig = go.Figure()
#
#         # Plot historical data
#         fig.add_trace(go.Scatter(
#             x=dates_past,
#             y=historical_data[category],
#             mode='lines+markers',
#             name='Actual',
#             line=dict(color='blue')
#         ))
#
#         # Plot forecast data
#         fig.add_trace(go.Scatter(
#             x=dates_future,
#             y=forecast_data[category],
#             mode='lines+markers',
#             name='Forecast',
#             line=dict(color='green', dash='dash')
#         ))
#
#         fig.update_layout(
#             title=f"  ",
#             xaxis_title="Date",
#             yaxis_title="Number of Transactions",
#             template="plotly_white",
#             hovermode='x unified'
#         )
#         return fig

def generate_sample_timeseries_with_ci(product):
    today = pd.Timestamp.today().normalize()
    past_days = pd.date_range(today - pd.Timedelta(days=29), today - pd.Timedelta(days=1))
    future_days = pd.date_range(today, today + pd.Timedelta(days=6))

    past_values = np.random.randint(5000, 10000, len(past_days))
    forecast_base = past_values[-1]
    forecast_values = forecast_base + np.cumsum(np.random.randint(-500, 500, len(future_days)))

    # Confidence intervals: ±10%
    lower_bound = forecast_values * 0.90
    upper_bound = forecast_values * 1.10

    df_past = pd.DataFrame({
        "Date": past_days,
        "Amount": past_values,
        "Type": "Actual"
    })

    df_future = pd.DataFrame({
        "Date": future_days,
        "Amount": forecast_values,
        "Lower": lower_bound,
        "Upper": upper_bound,
        "Type": "Forecast"
    })

    df_past["Product"] = product
    df_future["Product"] = product

    return df_past, df_future

def register_analytics_callback(app):
    @app.callback(
        Output("amount-growth-linechart", "figure"),
        Input("amount-category-selection-dropdown", "value")
    )
    def update_amount_growth_linechart(product):
        if not product:
            return go.Figure()

        df_past, df_future = generate_sample_timeseries_with_ci(product)

        fig = go.Figure()

        # Actual Line
        fig.add_trace(go.Scatter(
            x=df_past["Date"], y=df_past["Amount"],
            mode="lines+markers",
            name="Actual",
            line=dict(color="blue")
        ))

        # Forecast Line
        fig.add_trace(go.Scatter(
            x=df_future["Date"], y=df_future["Amount"],
            mode="lines+markers",
            name="Forecast",
            line=dict(color="green", dash="dash")
        ))

        # Confidence Interval: Shaded region
        fig.add_trace(go.Scatter(
            x=pd.concat([df_future["Date"], df_future["Date"][::-1]]),
            y=pd.concat([df_future["Upper"], df_future["Lower"][::-1]]),
            fill='toself',
            fillcolor='rgba(0, 200, 0, 0.1)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            name="Confidence Interval",
            showlegend=True
        ))

        fig.update_layout(
            title=f"{product} — Forecast with Confidence Interval",
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
    def update_volume_growth_linechart(product):
        if not product:
            return go.Figure()

        df_past, df_future = generate_sample_timeseries_with_ci(product)

        fig = go.Figure()

        # Actual Line
        fig.add_trace(go.Scatter(
            x=df_past["Date"], y=df_past["Amount"],
            mode="lines+markers",
            name="Actual",
            line=dict(color="blue")
        ))

        # Forecast Line
        fig.add_trace(go.Scatter(
            x=df_future["Date"], y=df_future["Amount"],
            mode="lines+markers",
            name="Forecast",
            line=dict(color="green", dash="dash")
        ))

        # Confidence Interval: Shaded region
        fig.add_trace(go.Scatter(
            x=pd.concat([df_future["Date"], df_future["Date"][::-1]]),
            y=pd.concat([df_future["Upper"], df_future["Lower"][::-1]]),
            fill='toself',
            fillcolor='rgba(0, 200, 0, 0.1)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            name="Confidence Interval",
            showlegend=True
        ))

        fig.update_layout(
            title=f"{product} — Past 30 days + 7 days Forecast",
            xaxis_title="Date",
            yaxis_title="Transaction Amount (NPR)",
            hovermode="x unified",
            template="plotly_white"
        )

        return fig
