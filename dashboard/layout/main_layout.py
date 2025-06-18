from dash import dcc, html
import dash_bootstrap_components as dbc


# Module Imports

def create_main_layout():
    return dbc.Container([
            html.H1("Transaction & Growth Forecast Dashboard", className="text-center my-4"),

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