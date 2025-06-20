from dash import html, dcc


amount_growth_linechart = html.Div([
        dcc.Graph(id='amount-growth-linechart')
    ])

volume_growth_linechart = html.Div([
        dcc.Graph(id='volume-growth-linechart')
    ])
