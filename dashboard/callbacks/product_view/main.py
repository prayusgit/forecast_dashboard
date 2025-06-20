# Module Imports
from .dropdown_callback import register_dropdown_callback
from .product_growth_linechart import register_growth_linechart_callback


def register_product_view_callbacks(app):
    register_dropdown_callback(app)
    register_growth_linechart_callback(app)