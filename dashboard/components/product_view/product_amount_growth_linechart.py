# Default imports
from dash import html, dcc

product_amount_growth_linechart = html.Div(
        dcc.Graph(id='product-amount-growth-linechart')
    )