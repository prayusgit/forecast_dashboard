# Default Imports
from dash import html, dcc, Input, Output

# Module imports
from layout.forecast_analytics.category_view.main import create_category_view_layout
from layout.forecast_analytics.product_view.main import create_product_view_layout
from .category_view.main import register_category_view_callbacks
from .product_view.main import register_product_view_callbacks


def register_callbacks(app):
    @app.callback(
        Output('tabs-content', 'children'),
        Input('forecast-tabs', 'active_tab')
    )
    def render_tab_content(tab):
        if tab == 'category-view':
            return create_category_view_layout()
        elif tab == 'product-view':
            return create_product_view_layout()

    register_category_view_callbacks(app)
    register_product_view_callbacks(app)

