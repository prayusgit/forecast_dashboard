# Default imports
from dash import html, dcc
import dash_bootstrap_components as dbc



category_email_section = html.Div([
    dbc.Input(id="category-recipient-email", type="email", placeholder="Enter recipient email", className="mt-3 mb-2",
              debounce=True),

    html.Button("Send Report to Email", id="category-email-send-btn",className='btn btn-outline-primary btn-block mb-2'),

    # Loading spinner (wrap modal inside so it waits for output)
    dcc.Loading(
        id="category-email-loading-spinner",
        type="circle",
        fullscreen=False,
        children=html.Div([
            # Modal popup
            dbc.Modal([
                dbc.ModalHeader("Email Status"),
                dbc.ModalBody(id="category-email-modal-body"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="category-email-close-modal", className="ms-auto", n_clicks=0)
                ),
            ],
                id="category-email-modal",
                is_open=False)
        ])
    ),
])