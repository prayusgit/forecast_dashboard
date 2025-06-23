# Default Imports
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input
import pandas as pd
from datetime import datetime, timedelta
import random
import requests




response = requests.get('http://127.0.0.1:8000/api/calender/festivals_within_7_days')
festivals = {
    key: datetime.strptime(value, "%Y-%m-%d").date()
    for key, value in response.json().items()
}


def register_alert_callback(app):
    @app.callback(
        Output('alert-output', 'children'),
        Input('alert-output', 'id')  # Trigger on page load
    )
    def generate_alerts(_):
        alerts = []
        now  = datetime.today().date()

        # 1. Festival Alerts (same as before)
        for fest_name, fest_date in festivals.items():
            days_diff = (fest_date - now).days
            if 0 <= days_diff <= 7:
                alerts.append(
                    dbc.Alert(f"✨ {fest_name} is in {days_diff} day(s). Expect transactional spike!", color="info")
                )


        prediction_alerts = requests.get('http://127.0.0.1:8000/api/category/transaction-alerts').json()['alerts']
        alerts.extend([dbc.Alert("🔮 " + alert_msg, color=color) for _, color, alert_msg in prediction_alerts])

        return alerts