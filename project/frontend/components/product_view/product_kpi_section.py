# Default Imports
import dash
from dash import html
import dash_bootstrap_components as dbc


product_kpi_section = dbc.Row([
    html.Div(className='col-3'),
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Small("Revenue Forecast for Next 7 days", className="text-muted"),
                html.H4(id='kpi-product-transaction-amount', className="card-title mb-0"),
            ])
        ], className="shadow-sm h-100"),
        width=3
    ),
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Small("Comparison with Current Week (WoW)", className="text-muted"),
                html.H4(id='kpi-product-wow-growth', className="card-title mb-0"),
            ])
        ], className="shadow-sm h-100"),
        width=3
    ),

], className="my-1 g-4")

