# Default Imports
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input
import pandas as pd
from datetime import datetime, timedelta
import random
import requests






def register_alert_callback(app):
    @app.callback(
        Output('alert-output', 'children'),
        Input('alert-output', 'id')  # Trigger on page load
    )
    def generate_alerts(_):
        alerts = []
        now = datetime.today().date()

        response = requests.get('http://127.0.0.1:8000/api/calender/festivals_within_7_days')
        data = response.json()
        festivals = {
            key: datetime.strptime(value, "%Y-%m-%d").date()
            for key, value in data.items()
        }

        # 1. Festival Alerts (same as before)
        for fest_name, fest_date in festivals.items():
            alerts.append(
                dbc.Alert(f"✨ {fest_name} is in {days_diff} day(s). Expect transactional spike!", color="info")
            )


        prediction_alerts = requests.get('http://127.0.0.1:8000/api/category/transaction-alerts').json()['alerts']
        alerts.extend([dbc.Alert("🔮 " + alert_msg, color=color) for _, color, alert_msg in prediction_alerts])

        return alerts