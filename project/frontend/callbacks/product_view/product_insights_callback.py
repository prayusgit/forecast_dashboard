# Default Imports
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input, State
import dash
import requests


def register_product_insights_callback(app):
    @app.callback(
        [Output("insights-modal-product", "is_open"),
         Output("insights-modal-product", "children"),
         Output("spinner-output-product", "children")],
        [Input("insights-btn-product", "n_clicks"),
         Input("close-insights-modal-product", "n_clicks")],
        [State("insights-modal-product", "is_open"),
         State("product-view-category-dropdown", "value"),
         State("product-view-product-dropdown", "value")])
    def toggle_product_insights_modal(open_clicks, close_clicks, is_open, selected_category, selected_product):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
        modal_content = [
            dbc.ModalHeader(dbc.ModalTitle("Product Insights")),
            dbc.ModalBody("Loading insights..."),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-insights-modal-product", className="ms-auto", n_clicks=0)
            ),
        ]
        
        if trigger_id == "insights-btn-product" and open_clicks:
            if not selected_category or not selected_product:
                modal_content = [
                    dbc.ModalHeader(dbc.ModalTitle("Product Insights")),
                    dbc.ModalBody("Please select both category and product to generate insights."),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close-insights-modal-product", className="ms-auto", n_clicks=0)
                    ),
                ]
                return True, modal_content, ""
            
            try:
                api_url = "http://localhost:8000/api/insight/chart-insight-product"
                response = requests.post(api_url, json={
                    "category": selected_category,
                    "product": selected_product
                })
                
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
                        dbc.ModalHeader(dbc.ModalTitle("Product Insights")),
                        dbc.ModalBody(insight_texts),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-insights-modal-product", className="ms-auto", n_clicks=0)
                        ),
                    ]
                else:
                    modal_content = [
                        dbc.ModalHeader(dbc.ModalTitle("Product Insights")),
                        dbc.ModalBody(f"Error: {response.text}"),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-insights-modal-product", className="ms-auto", n_clicks=0)
                        ),
                    ]
            except Exception as e:
                modal_content = [
                    dbc.ModalHeader(dbc.ModalTitle("Product Insights")),
                    dbc.ModalBody(f"Error: {str(e)}"),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close-insights-modal-product", className="ms-auto", n_clicks=0)
                    ),
                ]
            return True, modal_content, ""
        elif trigger_id == "close-insights-modal-product" and close_clicks:
            return False, modal_content, ""
        return is_open, modal_content, "" 