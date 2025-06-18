import dash
from dash import html, dcc
import dash

dash.register_page(__name__, path='/')

# Card style dictionary
card_style = {
    'width': '300px',
    'height': '250px',
    'margin': '20px',
    'padding': '20px',
    'border-radius': '10px',
    'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
    'transition': '0.3s',
    'background-color': 'white',
    'display': 'flex',
    'flex-direction': 'column',
    'align-items': 'center',
    'justify-content': 'center',
    'cursor': 'pointer',
}

# Hover style
hover_style = {
    'transform': 'scale(1.05)',
    'box-shadow': '0 8px 16px 0 rgba(0,0,0,0.2)',
}

layout = html.Div([
    
    # Cards container
    html.Div([
        # Transaction Analytics Card
        dcc.Link(
            html.Div([
                html.I(className='fas fa-chart-line', style={
                    'font-size': '48px',
                    'color': '#2E7D32',
                    'margin-bottom': '20px'
                }),
                html.H3('Transaction Analytics', style={
                    'text-align': 'center',
                    'color': '#2E7D32',
                    'margin-bottom': '10px'
                }),
                html.P('Analyze transaction patterns, volumes, and trends', style={
                    'color': '#666',
                    'text-align': 'center'
                })
            ], style=card_style),
            href='dashboard',
            style={'text-decoration': 'none'}
        ),
        
        # Prediction Card
        dcc.Link(
            html.Div([
                html.I(className='fas fa-brain', style={
                    'font-size': '48px',
                    'color': '#1976D2',
                    'margin-bottom': '20px'
                }),
                html.H3('Prediction', style={
                    'color': '#1976D2',
                    'margin-bottom': '10px'
                }),
                html.P('Forecast future transaction patterns and trends', style={
                    'color': '#666',
                    'text-align': 'center'
                })
            ], style=card_style),
            href='prediction',
            style={'text-decoration': 'none'}
        ),
        
        # Reports Card
        dcc.Link(
            html.Div([
                html.I(className='fas fa-file-alt', style={
                    'font-size': '48px',
                    'color': '#D32F2F',
                    'margin-bottom': '20px'
                }),
                html.H3('Reports', style={
                    'color': '#D32F2F',
                    'margin-bottom': '10px'
                }),
                html.P('Generate detailed reports and insights', style={
                    'color': '#666',
                    'text-align': 'center'
                })
            ], style=card_style),
            href='reports',
            style={'text-decoration': 'none'}
        ),
    ], style={
        'display': 'flex',
        'justify-content': 'center',
        'flex-wrap': 'wrap',
        'padding': '20px'
    }),
], style={
    'min-height': '100vh',
    'background-color': '#f5f5f5'
}) 