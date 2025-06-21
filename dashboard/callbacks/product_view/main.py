# Module Imports
from .product_growth_linechart_callback import register_growth_linechart_callback
from .product_comparison_callback import register_product_comparison_callback


def register_product_view_callbacks(app):
    register_growth_linechart_callback(app)
    register_product_comparison_callback(app)