# Default Imports
from dash import dcc, html, page_container
import dash_bootstrap_components as dbc


def create_main_layout():
    return  html.Div([
    # Header
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dcc.Link(
                    html.Img(
                        src='/frontend/assets/img/esewa-icon-large.png',
                        height='50px'  # Minimal styling
                    ),
                    href='/frontend'
                )
            ], width='auto'),

            dbc.Col([
                html.H3("eSewa Analytics Platform", className="mb-0")
            ], width='auto', className='d-flex align-items-center')
        ], className='py-3 border-bottom')
    ], className='my-2'),

    # Main content area
    page_container
])