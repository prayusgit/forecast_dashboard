# Default imports
import pandas as pd
from datetime import datetime, timedelta
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import requests


def generate_wow_growth_table():
    dates_past = pd.date_range(end=datetime.today(), periods=14)
    dates_future = pd.date_range(start=datetime.today() + timedelta(days=1), periods=7)
    categories = ["NTC Topup", "Ncell Topup", "Electricity", "Internet Payment"]

    data = []
    for cat in categories:
        for date in dates_past:
            data.append({"date": date, "category": cat, "amount": 900 + hash(str(cat) + str(date)) % 400})
        for date in dates_future:
            data.append({"date": date, "category": cat, "amount": 950 + hash("future" + str(cat) + str(date)) % 350})

    df = pd.DataFrame(data)

    today = datetime.today().date()
    this_week = df[(df["date"].dt.date <= today) & (df["date"].dt.date > today - timedelta(days=7))]
    next_week = df[(df["date"].dt.date > today) & (df["date"].dt.date <= today + timedelta(days=7))]

    results = []
    for cat in df["category"].unique():
        past_sum = this_week[this_week["category"] == cat]["amount"].sum()
        future_sum = next_week[next_week["category"] == cat]["amount"].sum()
        growth = ((future_sum - past_sum) / past_sum * 100) if past_sum > 0 else 0

        results.append({
            "Category": cat,
            "Week Forecast (Rs)": round(future_sum, 2),
            "WoW Growth (%)": round(growth, 2)
        })

    return pd.DataFrame(results)


# --- Callback with no inputs: triggered automatically on load
def register_dash_table_callback(app):
    @app.callback(
        Output("wow-growth-table", "children"),
        Input('wow-multi-category-selection-dropdown', 'value')
    )
    def display_growth_table(categories):
        response = requests.post('http://127.0.0.1:8000/api/category/wow-growth', json={'req_categories':categories}).json()['wow_growth_list']
        df = pd.DataFrame(response, columns=["Category", "Week Forecast (Rs)", "WoW Growth (%)"])
        print(df)
        return dash_table.DataTable(
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict("records"),
            style_cell={
                'textAlign': 'center',
                'padding': '10px',
                'font-family': 'Arial',
            },
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{WoW Growth (%)} > 0',
                        'column_id': 'WoW Growth (%)'
                    },
                    'color': 'green',
                    'fontWeight': 'bold'
                },
                {
                    'if': {
                        'filter_query': '{WoW Growth (%)} < 0',
                        'column_id': 'WoW Growth (%)'
                    },
                    'color': 'red',
                    'fontWeight': 'bold'
                },
            ],
            style_table={'overflowX': 'auto'},
            page_size=10
        )

    @app.callback(
        Output('wow-multi-category-selection-dropdown', 'options'),
        Output('wow-multi-category-selection-dropdown', 'value'),
        Input('wow-multi-category-selection-dropdown', 'id')
    )
    def update_multi_dropdown(_):
        categories = requests.get('http://127.0.0.1:8000/api/info/categories').json()['categories']
        options = [{'label': cat, 'value': cat} for cat in categories]
        return options, categories[:5]

