# Default Imports
from dash import dcc, html

category_to_products = {
    "Topup": ["NTC Topup", "Ncell Topup"],
    "Bill Payment": ["Electricity Bill", "Khanepani Bill", "TV Recharge"],
    "Banking": ["P2P Transfer", "Bank Withdrawal"],
    "Insurance": ["Insurance Premium"]
}

product_view_category_dropdown = html.Div([
            html.Label("Select Category:"),
            dcc.Dropdown(
                id="product-view-category-dropdown",
                options=[{"label": k, "value": k} for k in category_to_products.keys()],
                placeholder="Choose a category",
                value="Topup",  # Optional default
                clearable=False
            )
        ], className='mb-2')


product_view_product_dropdown = html.Div([
            html.Label("Select Product:"),
            dcc.Dropdown(
                id="product-view-product-dropdown",
                placeholder="Choose one or more products",
            )
        ])