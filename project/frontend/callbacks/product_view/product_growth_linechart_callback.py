# Default Imports
from dash import Input, Output, html
import plotly.graph_objects as go
import pandas as pd
import requests

# Module Imports
from utils.helper_functions import format


def colored_text(value):
    color = "success" if value >= 0 else "danger"
    sign = "+" if value >= 0 else "-"
    return html.Span(f"{sign}{abs(value):.1f}%", className=f"text-{color} ms-2")


def register_growth_linechart_callback(app):
    @app.callback(
        Output('kpi-product-transaction-amount', 'children'),
        Output('kpi-product-wow-growth', 'children'),
        Input('product-data-store', 'data')
    )
    def update_product_kpi(data):
        df_past = pd.DataFrame(data['past_data'])
        df_future = pd.DataFrame(data['future_data'])

        current_week = df_past.iloc[-7:]['transaction_amount'].sum()

        predicted_next_week = df_future['transaction_amount'].sum() # 7 days forecast (model simulation)

        growth = ((predicted_next_week - current_week) / current_week) * 100

        growth = round(growth, 1)

        return "NPR " + format(predicted_next_week), colored_text(growth)


    @app.callback(
        Output("product-amount-growth-linechart", "figure"),
        Output('product-data-store', 'data'),
        Input("product-view-category-dropdown", "value"),
        Input("product-view-product-dropdown", "value")
    )
    def update_line_chart(category, product):
        if not category:
            return go.Figure()

            # API call
        response = requests.get(
            f'http://127.0.0.1:8000/api/product/forecast/product-amount/{category}/{product}').json()

        # Load data
        df_actual = pd.DataFrame(response['past_data_actual'])  # actual
        df_forecast = pd.DataFrame(response['past_data_forecast'])  # forecast
        df_future = pd.DataFrame(response['future_data_forecast'])  # next 7 days

        # Date conversion
        df_actual['transaction_date'] = pd.to_datetime(df_actual['transaction_date'])
        df_forecast['transaction_date'] = pd.to_datetime(df_forecast['transaction_date'])
        df_future['transaction_date'] = pd.to_datetime(df_future['transaction_date'])

        # Merge actual and forecast on date to compare
        df_compare = pd.merge(df_actual, df_forecast, on='transaction_date', suffixes=('_actual', '_pred'))

        # Calculate prediction error (%)
        df_compare['error_pct'] = ((df_compare['transaction_amount_pred'] - df_compare['transaction_amount_actual']) /
                                   df_compare['transaction_amount_actual']) * 100

        # Identify large errors (> 50%)
        df_compare['large_error'] = df_compare['error_pct'].abs() > 50

        # Start plotting
        fig = go.Figure()

        # Actual Line (Blue)
        fig.add_trace(go.Scatter(
            x=df_compare['transaction_date'],
            y=df_compare['transaction_amount_actual'],
            mode='lines+markers',
            name='Actual',
            line=dict(color='blue')
        ))

        # Predicted Line (Green)
        fig.add_trace(go.Scatter(
            x=df_compare['transaction_date'],
            y=df_compare['transaction_amount_pred'],
            mode='lines+markers',
            name='Predicted',
            line=dict(color='orange'),
        ))

        # Large Error Points (Red markers)
        df_errors = df_compare[df_compare['large_error']]
        fig.add_trace(go.Scatter(
            x=df_errors['transaction_date'],
            y=df_errors['transaction_amount_pred'],
            mode='markers',
            name='Large Errors (>50%)',
            marker=dict(color='red', size=10, symbol='x'),
            hoverinfo='skip'

        ))

        # Forecast (Future) Line
        fig.add_trace(go.Scatter(
            x=df_future["transaction_date"],
            y=df_future["transaction_amount"],
            mode="lines+markers",
            name="Future Forecast",
            line=dict(color="green", dash="dot")
        ))

        # Confidence interval
        fig.add_trace(go.Scatter(
            x=pd.concat([df_future["transaction_date"], df_future["transaction_date"][::-1]]),
            y=pd.concat([df_future["upper"], df_future["lower"][::-1]]),
            fill='toself',
            fillcolor='rgba(0, 200, 0, 0.1)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            name="Confidence Interval",
            showlegend=True
        ))

        # Layout
        fig.update_layout(
            title=f"{product} — Actual vs Predicted Transactions with Forecast",
            xaxis_title="Date",
            yaxis_title="Transaction Amount (NPR)",
            hovermode="x",
            template="plotly_white"
        )

        return fig, {
            'past_data': df_actual.to_dict(),
            'future_data': df_future.to_dict()
        }

        if not product:
            return go.Figure()

        response = requests.get(f'http://127.0.0.1:8000/api/product/forecast/product-amount/{category}/{product}').json()

        df_past, df_future = pd.DataFrame(response['past_data']), pd.DataFrame(response['future_data'])

        df_past['transaction_date'] = pd.to_datetime(df_past['transaction_date'])
        df_future['transaction_date'] = pd.to_datetime(df_future['transaction_date'])

        fig = go.Figure()

        # Actual Line
        fig.add_trace(go.Scatter(
            x=df_past["transaction_date"], y=df_past["transaction_amount"],
            mode="lines+markers",
            name="Actual",
            line=dict(color="blue")
        ))

        # Forecast Line
        fig.add_trace(go.Scatter(
            x=df_future["transaction_date"], y=df_future["transaction_amount"],
            mode="lines+markers",
            name="Forecast",
            line=dict(color="green", dash="dash")
        ))

        # Confidence Interval: Shaded region
        fig.add_trace(go.Scatter(
            x=pd.concat([df_future["transaction_date"], df_future["transaction_date"][::-1]]),
            y=pd.concat([df_future["upper"], df_future["lower"][::-1]]),
            fill='toself',
            fillcolor='rgba(0, 200, 0, 0.1)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            name="Confidence Interval",
            showlegend=True
        ))

        fig.update_layout(
            title=f"{product} — Past 30 days + 7 days Forecast",
            xaxis_title="Date",
            yaxis_title="Transaction Amount (NPR)",
            hovermode="x unified",
            template="plotly_white"

        )



    @app.callback(
        Output('product-view-category-dropdown', 'options'),
        Output('product-view-category-dropdown', 'value'),
        Input('product-view-category-dropdown', 'id')
    )
    def update_volume_category_dropdown(_):
        categories = requests.get('http://127.0.0.1:8000/api/info/categories').json()['categories']
        options = [{'label': cat, 'value': cat} for cat in categories]
        return options, categories[0]

    @app.callback(
        Output("product-view-product-dropdown", "options"),
        Output("product-view-product-dropdown", "value"),
        Input("product-view-category-dropdown", "value")
    )
    def update_product_dropdown(category):
        if category:
            response = requests.get(f'http://127.0.0.1:8000/api/info/category_to_products/{category}').json()
            products = response['products']
            options = [{"label": p, "value": p} for p in products]
            return options, products[0]  # pre-select all products by default
        return [], []





