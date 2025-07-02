# Default Imports
from dash import dcc, html, Input, Output, State
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
import dash_bootstrap_components as dbc
import dash

API_BASE_URL = "http://localhost:8000"

def register_analytics_callback(app):
    @app.callback(
        Output("amount-growth-linechart", "figure"),
        Input("amount-category-selection-dropdown", "value")
    )
    def update_amount_growth_linechart(category):
        if not category:
            return go.Figure()

            # API call
        response = requests.get(f'http://127.0.0.1:8000/api/category/forecast/category-amount/{category}').json()

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

        # Identify large errors (> 20%)
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
            title=f"{category} — Actual vs Predicted Transactions with Forecast",
            xaxis_title="Date",
            yaxis_title="Transaction Amount (NPR)",
            hovermode="x",
            template="plotly_white"
        )

        return fig


    @app.callback(
        Output("volume-growth-linechart", "figure"),
        Input("volume-category-selection-dropdown", "value")
    )
    def update_volume_growth_linechart(category):
        if not category:
            return go.Figure()

            # API call
        response = requests.get(f'http://127.0.0.1:8000/api/category/forecast/category-count/{category}').json()

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
        df_compare['error_pct'] = ((df_compare['transaction_count_pred'] - df_compare['transaction_count_actual']) /
                                   df_compare['transaction_count_actual']) * 100

        # Identify large errors (> 20%)
        df_compare['large_error'] = df_compare['error_pct'].abs() > 50

        # Start plotting
        fig = go.Figure()

        # Actual Line (Blue)
        fig.add_trace(go.Scatter(
            x=df_compare['transaction_date'],
            y=df_compare['transaction_count_actual'],
            mode='lines+markers',
            name='Actual',
            line=dict(color='blue')
        ))

        # Predicted Line (Green)
        fig.add_trace(go.Scatter(
            x=df_compare['transaction_date'],
            y=df_compare['transaction_count_pred'],
            mode='lines+markers',
            name='Predicted',
            line=dict(color='orange'),
        ))

        # Large Error Points (Red markers)
        df_errors = df_compare[df_compare['large_error']]
        fig.add_trace(go.Scatter(
            x=df_errors['transaction_date'],
            y=df_errors['transaction_count_pred'],
            mode='markers',
            name='Large Errors (>50%)',
            marker=dict(color='red', size=10, symbol='x'),
            hoverinfo='skip'

        ))

        # Forecast (Future) Line
        fig.add_trace(go.Scatter(
            x=df_future["transaction_date"],
            y=df_future["transaction_count"],
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
            title=f"{category} — Actual vs Predicted Transactions with Forecast",
            xaxis_title="Date",
            yaxis_title="Transaction Count",
            hovermode="x",
            template="plotly_white"
        )

        return fig

    @app.callback(
        Output('amount-category-selection-dropdown', 'options'),
        Output('amount-category-selection-dropdown', 'value'),
        Input('amount-category-selection-dropdown', 'id')
    )
    def update_amount_category_dropdown(_):
        categories = requests.get('http://127.0.0.1:8000/api/info/categories').json()['categories']
        options = [{'label': cat, 'value': cat} for cat in categories]
        return options, categories[0]

    @app.callback(
        Output('volume-category-selection-dropdown', 'options'),
        Output('volume-category-selection-dropdown', 'value'),
        Input('volume-category-selection-dropdown', 'id')
    )
    def update_volume_category_dropdown(_):
        categories = requests.get('http://127.0.0.1:8000/api/info/categories').json()['categories']
        options = [{'label': cat, 'value': cat} for cat in categories]
        return options, categories[0]


def register_insights_modal_callback(app):
    @app.callback(
        [Output("insights-modal-volume", "is_open"),
         Output("insights-modal-volume", "children")],
        [Input("insights-btn-volume", "n_clicks"), Input("close-insights-modal-volume", "n_clicks")],
        [State("insights-modal-volume", "is_open"),
         State("amount-category-selection-dropdown", "value")],
    )
    def toggle_modal_volume(open_clicks, close_clicks, is_open, selected_category):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
        modal_content = [
            dbc.ModalHeader(dbc.ModalTitle("Insight")),
            dbc.ModalBody("this is insight"),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-insights-modal-volume", className="ms-auto", n_clicks=0)
            ),
        ]
        if trigger_id == "insights-btn-volume" and open_clicks:
            try:
                api_url = "http://localhost:8000/api/insight/chart-insight-volume"
                response = requests.post(api_url, json={"category": selected_category})
                if response.status_code == 200:
                    data = response.json()
                    insights = data.get("insights", {})
                    color_map = {
                        "executive": "primary",
                        "marketing": "success",
                        "engineering": "warning",
                        "non-tech": "info"
                    }
                    insight_texts = []
                    for user_type in ["executive", "marketing", "engineering", "non-tech"]:
                        insight = insights.get(user_type, {})
                        text = insight.get("insight_text", "No insight returned.")
                        insight_texts.append(
                            dbc.Alert([
                                html.H5(user_type.capitalize() + " Insight", className="mb-2"),
                                html.P(text)
                            ], color=color_map.get(user_type, "secondary"), className="mb-3")
                        )
                    modal_content = [
                        dbc.ModalHeader(dbc.ModalTitle("Insights")),
                        dbc.ModalBody(insight_texts),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-insights-modal-volume", className="ms-auto", n_clicks=0)
                        ),
                    ]
                else:
                    modal_content = [
                        dbc.ModalHeader(dbc.ModalTitle("Insight")),
                        dbc.ModalBody(f"Error: {response.text}"),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-insights-modal-volume", className="ms-auto", n_clicks=0)
                        ),
                    ]
            except Exception as e:
                modal_content = [
                    dbc.ModalHeader(dbc.ModalTitle("Insight")),
                    dbc.ModalBody(f"Error: {str(e)}"),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close-insights-modal-volume", className="ms-auto", n_clicks=0)
                    ),
                ]
            return True, modal_content
        elif trigger_id == "close-insights-modal-volume" and close_clicks:
            return False, modal_content
        return is_open, modal_content

    @app.callback(
        [Output("insights-modal-count", "is_open"),
         Output("insights-modal-count", "children")],
        [Input("insights-btn-count", "n_clicks"), Input("close-insights-modal-count", "n_clicks")],
        [State("insights-modal-count", "is_open"),
         State("volume-category-selection-dropdown", "value")],
    )
    def toggle_modal_count(open_clicks, close_clicks, is_open, selected_category):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
        modal_content = [
            dbc.ModalHeader(dbc.ModalTitle("Insight")),
            dbc.ModalBody("this is insight"),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-insights-modal-count", className="ms-auto", n_clicks=0)
            ),
        ]
        if trigger_id == "insights-btn-count" and open_clicks:
            try:
                api_url = "http://localhost:8000/api/insight/chart-insight-count"
                response = requests.post(api_url, json={"category": selected_category})
                if response.status_code == 200:
                    data = response.json()
                    insights = data.get("insights", {})
                    color_map = {
                        "executive": "primary",
                        "marketing": "success",
                        "engineering": "warning",
                        "non-tech": "info"
                    }
                    insight_texts = []
                    for user_type in ["executive", "marketing", "engineering", "non-tech"]:
                        insight = insights.get(user_type, {})
                        text = insight.get("insight_text", "No insight returned.")
                        insight_texts.append(
                            dbc.Alert([
                                html.H5(user_type.capitalize() + " Insight", className="mb-2"),
                                html.P(text)
                            ], color=color_map.get(user_type, "secondary"), className="mb-3")
                        )
                    modal_content = [
                        dbc.ModalHeader(dbc.ModalTitle("Insights")),
                        dbc.ModalBody(insight_texts),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-insights-modal-count", className="ms-auto", n_clicks=0)
                        ),
                    ]
                else:
                    modal_content = [
                        dbc.ModalHeader(dbc.ModalTitle("Insight")),
                        dbc.ModalBody(f"Error: {response.text}"),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-insights-modal-count", className="ms-auto", n_clicks=0)
                        ),
                    ]
            except Exception as e:
                modal_content = [
                    dbc.ModalHeader(dbc.ModalTitle("Insight")),
                    dbc.ModalBody(f"Error: {str(e)}"),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close-insights-modal-count", className="ms-auto", n_clicks=0)
                    ),
                ]
            return True, modal_content
        elif trigger_id == "close-insights-modal-count" and close_clicks:
            return False, modal_content
        return is_open, modal_content

