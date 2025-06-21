import dash
from dash import html
import dash_bootstrap_components as dbc


# KPI values
total_transactions = 67800
transactions_change = 8.2
total_volume = "NPR 12.5 Cr"
growth_rate_yoy = 12.5
forecast_confidence = 88


# Helper to color percentage
def colored_text(value):
    color = "success" if value >= 0 else "danger"
    sign = "+" if value >= 0 else "-"
    return html.Span(f"{sign}{abs(value):.1f}%", className=f"text-{color} ms-2")


# KPI Card Layout using Bootstrap grid
product_kpi_section = dbc.Row([
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Small("Forecast Revenue (NPR)", className="text-muted"),
                html.H4(f"{total_volume}", className="card-title mb-0"),
            ])
        ], className="shadow-sm h-100"),
        width=4
    ),
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Small("Growth Rate (WoW)", className="text-muted"),
                html.H4(colored_text(growth_rate_yoy), className="card-title mb-0"),
            ])
        ], className="shadow-sm h-100"),
        width=4
    ),

], className="my-4 g-4")

