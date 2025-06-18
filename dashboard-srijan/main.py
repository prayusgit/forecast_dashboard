import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash import page_registry, page_container


# Initialize the Dash app with multi-page support
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
    ]
)

# Define the main app layout with navigation
app.layout = html.Div([
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

# Run the app
if __name__ == '__main__':
    app.run(debug=True) 