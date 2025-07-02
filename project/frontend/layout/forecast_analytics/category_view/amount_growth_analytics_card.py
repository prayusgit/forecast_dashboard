# Default Imports
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Module Imports
from components.category_view.growth_analytics_linechart import amount_growth_linechart
from components.category_view.category_selection_dropdown import amount_category_selection_dropdown
from components.category_view.insights_button import insights_button_amount


def amount_growth_analytics_layout():
    return dbc.Card([
        dbc.CardHeader('Growth Analytics'),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(html.H4("📈 Revenue Growth Analytics"), width=8),
                dbc.Col(amount_category_selection_dropdown, width=4),

            ]),
            amount_growth_linechart,
            dbc.Row([
                html.Div(
                    "  ", className="col-8"),
                dbc.Col(insights_button_amount, width=4)
            ])
        ])
    ])



