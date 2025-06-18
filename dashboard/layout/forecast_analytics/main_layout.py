from dash import dcc, html
import dash_bootstrap_components as dbc


# Module Imports



def create_forecast_analytics_layout():
    return dbc.Container([
            html.H1("Forecast and Analytics Dashboard", className="text-center my-4",
                    style={'color': '#2E7D32'}),

            dbc.Tabs(id="forecast-tabs", active_tab='daily', children=[
                dbc.Tab(label='Short Term', tab_id='daily'),
                dbc.Tab(label='Long Term', tab_id='monthly'),
            ], className="mb-4"),

            # dbc.Card([
            #     dbc.CardHeader('Daily Forecast'),
            #     dbc.CardBody(id='tabs-content')
            # ], className="shadow-sm"),

            html.Div(id='tabs-content')
    ])