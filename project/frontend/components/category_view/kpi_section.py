# Default Imports
from dash import html
import dash_bootstrap_components as dbc



# KPI Card Layout using Bootstrap grid
kpi_section = dbc.Row([
    html.Div(className='col-3'),
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Small(["Number of Transactions", html.Span(id='kpi-day-label-1')], className="text-muted"),
                html.H4(id='kpi-category-transaction-count', className="card-title mb-0"),
            ])
        ], className="shadow-sm h-100"),
        width=3
    ),
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Small(["Forecast Amount", html.Span(id='kpi-day-label-2')], className="text-muted"),
                html.H4(id='kpi-category-transaction-amount', className="card-title mb-0"),
            ])
        ], className="shadow-sm h-100"),
        width=3
    )
], className="my-1 g-4")

