# Default Imports
from dash import html, dcc, Input, Output

# Module imports
from layout.daily.main import create_daily_layout
from layout.monthly.main import create_monthly_layout
from .daily.main import register_daily_callbacks
from .monthly.main import register_monthly_callbacks


def register_callbacks(app):
    @app.callback(
        Output('tabs-content', 'children'),
        Input('forecast-tabs', 'active_tab')
    )
    def render_tab_content(tab):
        if tab == 'daily':
            return create_daily_layout()
        elif tab == 'monthly':
            return create_monthly_layout()

    register_daily_callbacks(app)
    register_monthly_callbacks(app)