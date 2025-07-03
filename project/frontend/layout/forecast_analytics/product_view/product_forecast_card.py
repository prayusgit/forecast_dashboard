# Default Imports
from dash import html, dcc
import dash_bootstrap_components as dbc

# Module Imports
from components.product_view.product_category_dropdown import product_view_category_dropdown, product_view_product_dropdown
from components.product_view.product_amount_growth_linechart import product_amount_growth_linechart
from components.product_view.product_kpi_section import product_kpi_section
from components.product_view.insights_button_product import insights_button_product


def product_forecast_layout():
    return dbc.Card([
            dbc.CardHeader('Product Forecast Analytics'),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(html.H4("📈 Product Performance and Forecast"), width=8),
                    dbc.Col([
                        product_view_category_dropdown,
                        product_view_product_dropdown,
                        
                    ], width=4)
                ]),
                product_kpi_section,
                product_amount_growth_linechart,
                dbc.Row([
                html.Div(
                    "  ", className="col-8"),
                dbc.Col(insights_button_product, width=4)
            ])
            ])
        ])