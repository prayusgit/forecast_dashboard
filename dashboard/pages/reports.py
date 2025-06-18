import dash
from dash import html
import dash

dash.register_page(__name__)

layout = html.Div([
    html.Div([
        html.H2('Reports', style={
            'textAlign': 'center',
            'color': '#D32F2F',
            'marginBottom': '30px'
        }),
        html.P('Reports feature is under development!', style={
            'textAlign': 'center',
            'fontSize': '1.2em',
            'color': '#666'
        }),
        html.Div([
            html.I(className='fas fa-file-alt', style={
                'fontSize': '48px',
                'color': '#D32F2F',
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