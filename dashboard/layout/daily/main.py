import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output


def create_daily_layout():
    return html.Div([
            html.H4("📊 Daily Forecast Overview", className="mb-3"),
            dcc.Graph(id="daily-graph", figure={
                "layout": {"title": "Daily Transaction Prediction", "template": "plotly_white"}
            }),
            html.P("Includes predictions, actuals, and service breakdown for today.", className="text-muted")
        ])

