import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Insights button for volume/amount analytics

def insights_button_volume():
    return html.Div([
        dbc.Button("Insights", id="insights-btn-volume", color="info", className="me-2"),
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Insight")),
            dbc.ModalBody("this is insight"),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-insights-modal-volume", className="ms-auto", n_clicks=0)
            ),
        ], id="insights-modal-volume", is_open=False),
    ])

# Insights button for count/traffic analytics

def insights_button_count():
    return html.Div([
        dbc.Button("Insights", id="insights-btn-count", color="info", className="me-2"),
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Insight")),
            dbc.ModalBody("this is insight"),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-insights-modal-count", className="ms-auto", n_clicks=0)
            ),
        ], id="insights-modal-count", is_open=False),
    ]) 

insights_button_volume = insights_button_volume()
insights_button_count = insights_button_count()