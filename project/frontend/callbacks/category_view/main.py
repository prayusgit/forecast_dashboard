# Default Imports
from dash import html, dcc, Input, Output

# Module Imports
from .prediction_barchart_callback import register_prediction_callback
from .analytics_linechart_callback import register_analytics_callback
from .wow_growth_section_callback import register_dash_table_callback
from .alert_callback import register_alert_callback
from .kpi_callback import register_kpi_callback
from .data_store_callback import register_data_store_callback


def register_category_view_callbacks(app):
    register_prediction_callback(app)
    register_analytics_callback(app)
    register_dash_table_callback(app)
    register_alert_callback(app)
    register_kpi_callback(app)
    register_data_store_callback(app)

