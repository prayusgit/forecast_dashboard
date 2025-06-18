import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

dash.register_page(__name__)

# Load the dataset
df = pd.read_csv('synthetic_data.csv')

# Convert transaction_date to datetime
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

layout = html.Div([
    html.Div([
        html.H2('Transaction Analysis Dashboard', style={
            'textAlign': 'center',
            'color': '#2E7D32',
            'marginBottom': '30px'
        }),
        
        # Date dropdown in its own row
        dcc.Dropdown(
            id='date-dropdown',
            options=[
                {'label': 'All Dates', 'value': 'all'},
                *[{'label': date.strftime('%Y-%m-%d'), 'value': date.strftime('%Y-%m-%d')} 
                  for date in sorted(df['transaction_date'].unique())]
            ],
            value='all',
            style={'width': '50%', 'margin': '20px auto'}
        ),
        
        # Flex row for bar charts
        html.Div([
            # Transaction Volume Bar Chart
            html.Div([
                html.H3('Transaction Volume by Category', style={'color': '#2E7D32'}),
                dcc.Graph(id='category-bar-chart')
            ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20px'}),
            
            # Transaction Count Bar Chart
            html.Div([
                html.H3('Transaction Count by Category', style={'color': '#2E7D32'}),
                dcc.Graph(id='category-count-chart')
            ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20px'})
        ], style={'display': 'flex', 'flexDirection': 'row'}),

        # New row for the range slider chart
        html.Div([
            html.H3('Transaction Volume Over Time', style={'color': '#2E7D32'}),
            dcc.Dropdown(
                id='category-dropdown',
                options=[
                    {'label': 'All Categories', 'value': 'all'},
                    *[{'label': cat, 'value': cat} for cat in df['service_category'].unique()]
                ],
                value='all',
                style={'width': '50%', 'margin': '20px auto'}
            ),
            dcc.Graph(id='range-slider-chart')
        ], style={'width': '100%', 'padding': '0 20px'})
    ], style={'padding': '20px', 'backgroundColor': '#f5f5f5'})
])

# Bar chart for transaction volume
@callback(
    Output('category-bar-chart', 'figure'),
    [Input('date-dropdown', 'value')]
)
def update_bar_chart(selected_date):
    filtered_df = df.copy()
    if selected_date != 'all':
        filtered_df = filtered_df[filtered_df['transaction_date'].dt.strftime('%Y-%m-%d') == selected_date]
    category_data = filtered_df.groupby('service_category')['amount'].sum().reset_index()
    title = 'Transaction Volume by Category'
    if selected_date != 'all':
        title += f' on {selected_date}'
    fig = px.bar(
        category_data,
        x='service_category',
        y='amount',
        title=title,
        labels={'amount': 'Total Transaction Volume', 'service_category': 'Service Category'},
        color='service_category',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(
        xaxis_title='Service Category',
        yaxis_title='Total Transaction Volume',
        template='plotly_white',
        height=600,
        showlegend=False
    )
    return fig

# Bar chart for transaction count
@callback(
    Output('category-count-chart', 'figure'),
    [Input('date-dropdown', 'value')]
)
def update_count_chart(selected_date):
    filtered_df = df.copy()
    if selected_date != 'all':
        filtered_df = filtered_df[filtered_df['transaction_date'].dt.strftime('%Y-%m-%d') == selected_date]
    category_data = filtered_df.groupby('service_category').size().reset_index(name='count')
    title = 'Transaction Count by Category'
    if selected_date != 'all':
        title += f' on {selected_date}'
    fig = px.bar(
        category_data,
        x='service_category',
        y='count',
        title=title,
        labels={'count': 'Number of Transactions', 'service_category': 'Service Category'},
        color='service_category',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(
        xaxis_title='Service Category',
        yaxis_title='Number of Transactions',
        template='plotly_white',
        height=600,
        showlegend=False
    )
    return fig

# Range slider chart responds to category-dropdown
@callback(
    Output('range-slider-chart', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_range_slider_chart(selected_category):
    filtered_df = df.copy()
    if selected_category != 'all':
        filtered_df = filtered_df[filtered_df['service_category'] == selected_category]
    # Group by date, sum amount, and get the first non-null festival_name for each date
    df_volume = (
        filtered_df.groupby('transaction_date')
        .agg(amount=('amount', 'sum'), festival_name=('festival_name', 'first'))
        .reset_index()
    )
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_volume['transaction_date'],
            y=df_volume['amount'],
            mode='lines',
            name='Volume',
            customdata=df_volume['festival_name'],
            hovertemplate=(
                'Date: %{x|%b %d, %Y}<br>' +
                'Amount: %{y:,.0f}<br>' +
                'Festival: %{customdata}<extra></extra>'
            )
        )
    )
    fig.update_layout(
        height=500,
        margin=dict(l=50, r=50, t=50, b=50),
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True), 
            type="date"
        ),
        yaxis=dict(
            title='Transaction Volume',
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='Gray',
            tickformat=',.0f'
        ),
        xaxis_title='Date',
        template='plotly_white'
    )
    return fig 