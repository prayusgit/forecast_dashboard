from dash import dcc, html
import dash_bootstrap_components as dbc


def create_layout():
    return dbc.Container([
            html.H1("Transaction & Growth Forecast Dashboard", className="text-center my-4"),

            dbc.Tabs(id="forecast-tabs", active_tab='daily', children=[
                dbc.Tab(label='Daily Forecast', tab_id='daily'),
                dbc.Tab(label='Monthly Forecast', tab_id='monthly'),
            ], className="mb-4"),

            dbc.Card(dbc.CardBody(id='tabs-content'), className="shadow-sm")
        ])