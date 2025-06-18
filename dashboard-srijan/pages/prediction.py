import dash
from dash import html
import dash

dash.register_page(__name__)

layout = html.Div([
    html.Div([
        html.H2('Transaction Prediction', style={
            'textAlign': 'center',
            'color': '#1976D2',
            'marginBottom': '30px'
        }),
        html.P('This feature is coming soon!', style={
            'textAlign': 'center',
            'fontSize': '1.2em',
            'color': '#666'
        }),
        html.Div([
            html.I(className='fas fa-cogs', style={
                'fontSize': '48px',
                'color': '#1976D2',
                'marginBottom': '20px'
            })
        ], style={'textAlign': 'center', 'marginTop': '40px'})
    ], style={
        'padding': '40px',
        'backgroundColor': '#f5f5f5',
        'borderRadius': '10px',
        'margin': '40px auto',
        'maxWidth': '800px',
        'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.1)'
    })
]) 