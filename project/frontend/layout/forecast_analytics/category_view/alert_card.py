# Default Imports
from dash import dcc, html
import dash_bootstrap_components as dbc


def alert_notification_layout():
    return dbc.Card([
            dbc.CardHeader('Alert Notification'),
            dbc.CardBody([
                    html.Div(id='alert-output')
                ])
            ])