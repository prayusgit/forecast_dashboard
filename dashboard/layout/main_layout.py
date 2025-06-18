# Default Imports
from dash import dcc, html, page_container


def create_main_layout():
    return html.Div([
            # Header
            html.Div([
                # Header content with logo and title
                html.Div([
                    # Clickable Logo
                    dcc.Link(
                        html.Img(
                            src='/assets/img/esewa-icon-large.png',
                            style={
                                'height': '55px',
                                'marginRight': '15px',
                                'verticalAlign': 'middle',
                                'cursor': 'pointer'
                            }
                        ),
                        href='/'
                    ),
                    # Title
                    html.H1('eSewa Analytics Platform', style={
                        'color': '#2E7D32',
                        'display': 'inline',
                        'verticalAlign': 'middle'
                    })
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'flex-start',
                    'padding': '20px',
                    'marginLeft': '175px',
                    'marginRight': '175px',
                    'marginBottom': '20px',
                    'borderBottom': '2px solid #4CAF50'
                })
            ]),

            # Main content area
            page_container
        ])