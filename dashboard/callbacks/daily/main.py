# Default Imports
from dash import html, dcc, Input, Output

# Module Imports
from .prediction_barchart_callback import register_prediction_callback



def register_daily_callbacks(app):
    register_prediction_callback(app)
