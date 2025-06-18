# Default Imports
from dash import html, dcc
import dash


# Module imports
from layout.forecast_analytics.main_layout import create_forecast_analytics_layout

dash.register_page(__name__)

layout = create_forecast_analytics_layout()