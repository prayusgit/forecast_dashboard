# Default Imports
import dash_bootstrap_components as dbc
from dash import dcc, html

# Module Imports
from components.product_view.product_comparison_barchart import product_comparison_barchart
from components.product_view.multi_product_selection_dropdown import multi_product_selection_dropdown

def product_comparison_layout():
    return dbc.Card([
            dbc.CardHeader('Product Comparison Analytics'),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(html.H4("📊 Comparison of 7 Days Forecast With Other Products"), width=7),
                    dbc.Col(multi_product_selection_dropdown, width=5),
                ]),
                product_comparison_barchart
            ])
        ])