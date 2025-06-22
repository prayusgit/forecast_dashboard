import dash
from dash import html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dash_table import DataTable
import numpy as np

# --- Data Loading ---
df = pd.read_csv('dashboard/synthetic_data.csv')
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

# --- Dropdown Options ---
category_options = [
    {'label': cat, 'value': cat} for cat in sorted(df['service_category'].unique())
]
date_options = [
    {'label': 'All Dates', 'value': 'all'},
    *[{'label': date.strftime('%Y-%m-%d'), 'value': date.strftime('%Y-%m-%d')}
      for date in sorted(df['transaction_date'].unique())]
]

dash.register_page(__name__)

# --- Layout ---
layout = html.Div([
    html.Button("Download PDF", id="download-pdf-btn", n_clicks=0, style={"marginBottom": "20px"}),
    html.Div([
        html.H2('Interactive Report: Prediction & Growth Analytics', style={
            'textAlign': 'center',
            'color': '#1976D2',
            'marginBottom': '30px'
        }),
        html.Div(id='report-business-insights', style={'marginBottom': '40px'}),
        html.Div([
            html.Div([
                html.Label('Select Date:', style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='report-date-dropdown',
                    options=date_options,
                    value='all',
                    style={'width': '100%'}
                )
            ], style={'width': '48%', 'display': 'inline-block', 'paddingRight': '2%'}),
            html.Div([
                html.Label('Select Service Category:', style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='report-category-dropdown',
                    options=[{'label': 'All Categories', 'value': 'all'}] + category_options,
                    value='all',
                    style={'width': '100%'}
                )
            ], style={'width': '48%', 'display': 'inline-block'})
        ], style={'display': 'flex', 'marginBottom': '30px'}),
        html.Div([
            html.H4('Forecasted Transaction Amounts', style={'color': '#1976D2'}),
            dcc.Graph(id='report-forecast-bar-chart')
        ], style={'marginBottom': '40px'}),
        html.Div([
            html.H4('Growth Analytics Over Time', style={'color': '#1976D2'}),
            dcc.Graph(id='report-growth-line-chart')
        ], style={'marginBottom': '40px'}),
        html.Div([
            html.H4('Week-over-Week (WoW) Growth Summary', style={'color': '#1976D2'}),
            html.Div(id='report-wow-growth-table')
        ], style={'marginBottom': '40px'}),
    ], className='report-main-content', style={
        'padding': '40px',
        'backgroundColor': '#f5f5f5',
        'borderRadius': '10px',
        'margin': '40px auto',
        'maxWidth': '1000px',
        'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.1)'
    })
])

# --- Callbacks ---
@callback(
    Output('report-forecast-bar-chart', 'figure'),
    [Input('report-date-dropdown', 'value'), Input('report-category-dropdown', 'value')]
)
def update_forecast_bar_chart(selected_date, selected_category):
    """Update the forecast bar chart based on selected date and category."""
    filtered_df = df.copy()
    if selected_date != 'all':
        filtered_df = filtered_df[filtered_df['transaction_date'].dt.strftime('%Y-%m-%d') == selected_date]
    if selected_category != 'all':
        filtered_df = filtered_df[filtered_df['service_category'] == selected_category]
    # Forecast: use last 7 days rolling mean as next 3 days forecast
    forecast_days = 3
    forecast = []
    for cat in filtered_df['service_category'].unique():
        cat_df = filtered_df[filtered_df['service_category'] == cat].sort_values('transaction_date')
        if len(cat_df) < 7:
            continue
        last_date = cat_df['transaction_date'].max()
        rolling_mean = cat_df.set_index('transaction_date')['amount'].rolling(7).mean().dropna()
        if rolling_mean.empty:
            continue
        pred = rolling_mean.iloc[-1]
        for i in range(1, forecast_days + 1):
            forecast.append({
                'service_category': cat,
                'forecast_date': last_date + pd.Timedelta(days=i),
                'forecast_amount': pred
            })
    forecast_df = pd.DataFrame(forecast)
    if forecast_df.empty:
        return go.Figure()
    fig = px.bar(
        forecast_df,
        x='service_category',
        y='forecast_amount',
        color='service_category',
        text='forecast_amount',
        labels={'forecast_amount': 'Forecasted Amount', 'service_category': 'Service Category'},
        title='Forecasted Transaction Amounts (Next 3 Days)'
    )
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside', showlegend=False)
    fig.update_layout(yaxis_title='Amount (NPR)', xaxis_title='Service Category', height=500)
    return fig

@callback(
    Output('report-growth-line-chart', 'figure'),
    [Input('report-date-dropdown', 'value'), Input('report-category-dropdown', 'value')]
)
def update_growth_line_chart(selected_date, selected_category):
    """Update the growth analytics line chart based on selected date and category."""
    filtered_df = df.copy()
    if selected_date != 'all':
        filtered_df = filtered_df[filtered_df['transaction_date'].dt.strftime('%Y-%m-%d') == selected_date]
    if selected_category != 'all':
        filtered_df = filtered_df[filtered_df['service_category'] == selected_category]
    # Group by date and category
    group = filtered_df.groupby(['transaction_date', 'service_category'])['amount'].sum().reset_index()
    # Calculate rolling mean for growth trend
    group['rolling_mean'] = group.groupby('service_category')['amount'].transform(lambda x: x.rolling(7).mean())
    fig = go.Figure()
    for cat in group['service_category'].unique():
        cat_df = group[group['service_category'] == cat]
        fig.add_trace(go.Scatter(
            x=cat_df['transaction_date'],
            y=cat_df['amount'],
            mode='lines+markers',
            name=f'{cat} Actual',
            line=dict(width=2)
        ))
        fig.add_trace(go.Scatter(
            x=cat_df['transaction_date'],
            y=cat_df['rolling_mean'],
            mode='lines',
            name=f'{cat} 7D Avg',
            line=dict(dash='dash')
        ))
    fig.update_layout(
        title='Growth Analytics Over Time',
        xaxis_title='Date',
        yaxis_title='Amount (NPR)',
        template='plotly_white',
        height=500
    )
    return fig

@callback(
    Output('report-wow-growth-table', 'children'),
    [Input('report-date-dropdown', 'value')]
)
def update_wow_growth_table(selected_date):
    """Update the week-over-week growth summary table."""
    filtered_df = df.copy()
    if selected_date != 'all':
        filtered_df = filtered_df[filtered_df['transaction_date'].dt.strftime('%Y-%m-%d') == selected_date]
    today = filtered_df['transaction_date'].max()
    last_week = today - pd.Timedelta(days=7)
    this_week = filtered_df[(filtered_df['transaction_date'] > last_week) & (filtered_df['transaction_date'] <= today)]
    prev_week = filtered_df[(filtered_df['transaction_date'] > last_week - pd.Timedelta(days=7)) & (filtered_df['transaction_date'] <= last_week)]
    summary = []
    for cat in filtered_df['service_category'].unique():
        this_sum = this_week[this_week['service_category'] == cat]['amount'].sum()
        prev_sum = prev_week[prev_week['service_category'] == cat]['amount'].sum()
        growth = ((this_sum - prev_sum) / prev_sum * 100) if prev_sum > 0 else 0
        summary.append({
            'Service Category': cat,
            'This Week (NPR)': round(this_sum, 2),
            'WoW Growth (%)': round(growth, 2)
        })
    summary_df = pd.DataFrame(summary)
    if summary_df.empty:
        return html.Div('No data available.')
    return DataTable(
        columns=[{"name": col, "id": col} for col in summary_df.columns],
        data=summary_df.to_dict('records'),
        style_cell={'textAlign': 'center', 'padding': '10px', 'font-family': 'Arial'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        style_data_conditional=[
            {
                'if': {'filter_query': '{WoW Growth (%)} > 0', 'column_id': 'WoW Growth (%)'},
                'color': 'green', 'fontWeight': 'bold'
            },
            {
                'if': {'filter_query': '{WoW Growth (%)} < 0', 'column_id': 'WoW Growth (%)'},
                'color': 'red', 'fontWeight': 'bold'
            },
        ],
        style_table={'overflowX': 'auto'},
        page_size=10
    )

@callback(
    Output('report-business-insights', 'children'),
    [Input('report-date-dropdown', 'value'), Input('report-category-dropdown', 'value')]
)
def update_business_insights(selected_date, selected_category):
    """Update the key business insights section."""
    filtered_df = df.copy()
    if selected_date != 'all':
        filtered_df = filtered_df[filtered_df['transaction_date'].dt.strftime('%Y-%m-%d') == selected_date]
    if selected_category != 'all':
        filtered_df = filtered_df[filtered_df['service_category'] == selected_category]
    total_volume = filtered_df['amount'].sum()
    total_count = filtered_df.shape[0]
    avg_amount = filtered_df['amount'].mean() if total_count > 0 else 0
    # Growth rates
    today = filtered_df['transaction_date'].max()
    last_week = today - pd.Timedelta(days=7)
    this_week = filtered_df[(filtered_df['transaction_date'] > last_week) & (filtered_df['transaction_date'] <= today)]['amount'].sum()
    prev_week = filtered_df[(filtered_df['transaction_date'] > last_week - pd.Timedelta(days=7)) & (filtered_df['transaction_date'] <= last_week)]['amount'].sum()
    wow_growth = ((this_week - prev_week) / prev_week * 100) if prev_week > 0 else 0
    # Top/bottom categories
    cat_group = filtered_df.groupby('service_category')['amount'].sum().reset_index()
    top_cat = cat_group.sort_values('amount', ascending=False).head(1)
    bottom_cat = cat_group.sort_values('amount', ascending=True).head(1)
    insights = [
        html.Div([
            html.H4('Key Business Insights', style={'color': '#1976D2'}),
            html.Ul([
                html.Li(f"Total Transaction Volume: NPR {total_volume:,.0f}"),
                html.Li(f"Total Transaction Count: {total_count:,}"),
                html.Li(f"Average Transaction Size: NPR {avg_amount:,.2f}"),
                html.Li(f"Week-over-Week Growth: {wow_growth:.2f}%"),
                html.Li(f"Top Category: {top_cat['service_category'].values[0]} (NPR {top_cat['amount'].values[0]:,.0f})") if not top_cat.empty else None,
                html.Li(f"Lowest Category: {bottom_cat['service_category'].values[0]} (NPR {bottom_cat['amount'].values[0]:,.0f})") if not bottom_cat.empty else None,
            ])
        ], style={'marginBottom': '20px'})
    ]
    return insights 
    