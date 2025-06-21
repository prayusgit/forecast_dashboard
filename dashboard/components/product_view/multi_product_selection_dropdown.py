# Default Imports
from dash import dcc, html

multi_product_selection_dropdown = html.Div([
                html.Label("Select Products to Compare:"),
                dcc.Dropdown(
                    id="multi-product-selection-multi-dropdown",
                    multi=True,
                    placeholder="Choose products to compare"
                )
            ])
