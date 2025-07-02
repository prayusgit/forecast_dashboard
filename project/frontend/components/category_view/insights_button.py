from dash import html, dcc
import dash_bootstrap_components as dbc


insights_button_amount = html.Div([
        html.Button("Insights", id="insights-btn-amount", className="w-100 btn btn-outline-danger", n_clicks=0),

        html.Div(id="spinner-output-1", style={"display": "none"}),

        dcc.Loading(
            type="circle",
            fullscreen=True,
            children=[
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Insight")),
                        dbc.ModalBody("this is insight"),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-insights-modal-amount", className="ml-auto", n_clicks=0)
                        ),
                    ],
                    id="insights-modal-amount",
                    is_open=False,
                )
            ]
        )
    ])

insights_button_count = html.Div([
        html.Button("Insights", id="insights-btn-count", className="w-100 btn btn-outline-danger", n_clicks=0),

        html.Div(id="spinner-output-2", style={"display": "none"}),

        dcc.Loading(
            type="circle",
            fullscreen=True,
            children=[
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Insight")),
                        dbc.ModalBody("this is insight"),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-insights-modal-count", className="ml-auto", n_clicks=0)
                        ),
                    ],
                    id="insights-modal-count",
                    is_open=False,
                )
            ]
        )
    ])