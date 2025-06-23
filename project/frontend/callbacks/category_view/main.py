# Default Imports
from dash import html, dcc, Input, Output

# Module Imports
from .prediction_barchart_callback import register_prediction_callback
from .analytics_linechart_callback import register_analytics_callback
from .wow_growth_section_callback import register_dash_table_callback
from .alert_callback import register_alert_callback


def register_category_view_callbacks(app):
    register_prediction_callback(app)
    register_analytics_callback(app)
    register_dash_table_callback(app)
    register_alert_callback(app)
