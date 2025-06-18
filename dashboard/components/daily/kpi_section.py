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
kpi_section = dbc.Row([
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Small("Daily Transactions", className="text-muted"),
                html.H4([
                    f"{total_transactions:,}",
                    colored_text(transactions_change)
                ], className="card-title mb-0"),
            ])
        ], className="shadow-sm h-100"),
        width=3
    ),
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Small("Daily Volume (NPR)", className="text-muted"),
                html.H4(f"{total_volume}", className="card-title mb-0"),
            ])
        ], className="shadow-sm h-100"),
        width=3
    ),
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Small("Growth Rate (YoY)", className="text-muted"),
                html.H4(colored_text(growth_rate_yoy), className="card-title mb-0"),
            ])
        ], className="shadow-sm h-100"),
        width=3
    ),
    dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.Small("Forecast Confidence", className="text-muted"),
                    html.H4(f"{forecast_confidence}%", className="card-title mb-0"),
                ])
            ], className="shadow-sm h-100"),
            width=3
    )
], className="my-4 g-4")

