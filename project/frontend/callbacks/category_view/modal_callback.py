# Default Imports
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input, State
import dash
import requests


def register_insights_modal_callback(app):
    @app.callback(
        [Output("insights-modal-amount", "is_open"),
         Output("insights-modal-amount", "children"),
         Output("spinner-output-1", "children")],
        [Input("insights-btn-amount", "n_clicks"),
         Input("close-insights-modal-amount", "n_clicks")],
        [State("insights-modal-amount", "is_open"),
         State("amount-category-selection-dropdown", "value")])
    def toggle_amount_modal(open_clicks, close_clicks, is_open, selected_category):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
        modal_content = [
            dbc.ModalHeader(dbc.ModalTitle("Insight")),
            dbc.ModalBody("this is insight"),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-insights-modal-amount", className="ms-auto", n_clicks=0)
            ),
        ]
        if trigger_id == "insights-btn-amount" and open_clicks:
            try:
                api_url = "http://localhost:8000/api/insight/chart-insight-amount"
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
                            dbc.Button("Close", id="close-insights-modal-amount", className="ms-auto", n_clicks=0)
                        ),
                    ]
                else:
                    modal_content = [
                        dbc.ModalHeader(dbc.ModalTitle("Insight")),
                        dbc.ModalBody(f"Error: {response.text}"),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-insights-modal-amount", className="ms-auto", n_clicks=0)
                        ),
                    ]
            except Exception as e:
                modal_content = [
                    dbc.ModalHeader(dbc.ModalTitle("Insight")),
                    dbc.ModalBody(f"Error: {str(e)}"),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close-insights-modal-amount", className="ms-auto", n_clicks=0)
                    ),
                ]
            return True, modal_content, ""
        elif trigger_id == "close-insights-modal-amount" and close_clicks:
            return False, modal_content, ""
        return is_open, modal_content, ""

    @app.callback(
        [Output("insights-modal-count", "is_open"),
         Output("insights-modal-count", "children"),
         Output("spinner-output-2", "children")],
        [Input("insights-btn-count", "n_clicks"),
         Input("close-insights-modal-count", "n_clicks")],
        [State("insights-modal-count", "is_open"),
         State("volume-category-selection-dropdown", "value")])
    def toggle_count_modal(open_clicks, close_clicks, is_open, selected_category):
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
            return True, modal_content, ""
        elif trigger_id == "close-insights-modal-count" and close_clicks:
            return False, modal_content, ""
        return is_open, modal_content, ""

