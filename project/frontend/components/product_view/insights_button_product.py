from dash import html, dcc
import dash_bootstrap_components as dbc


insights_button_product = html.Div([
        html.Button("Insights", id="insights-btn-product", className="w-100 btn btn-outline-danger", n_clicks=0),

        html.Div(id="spinner-output-product", style={"display": "none"}),

        dcc.Loading(
            type="circle",
            fullscreen=True,
            children=[
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Product Insights")),
                        dbc.ModalBody("Loading insights..."),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-insights-modal-product", className="ml-auto", n_clicks=0)
                        ),
                    ],
                    id="insights-modal-product",
                    is_open=False,
                )
            ]
        )
    ])
