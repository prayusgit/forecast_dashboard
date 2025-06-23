# Default Imports
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input
import pandas as pd
from datetime import datetime, timedelta
import random
import requests

# Sample data generation for transactions
response = requests.get('http://127.0.0.1:8000/api/info/categories')
categories = response.json()['categories']

# categories = ['Ncell Topup', 'Electricity Bill', 'Khanepani Bill', 'TV Recharge', 'Internet Payment']
today = datetime.today().date()

# Generate 14 days of sample data
data = []
for i in range(14):
    date = today - timedelta(days=i)
    for cat in categories:
        data.append({
            'date': date,
            'category': cat,
            'transactions': random.randint(400, 1200)
        })
df = pd.DataFrame(data)

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
        now = today

        # 1. Festival Alerts (same as before)
        for fest_name, fest_date in festivals.items():
            days_diff = (fest_date - now).days
            if 0 <= days_diff <= 7:
                alerts.append(
                    dbc.Alert(f"✨ {fest_name} is in {days_diff} day(s). Expect transactional spike!", color="info")
                )

        # 2. Prediction Alerts (compare predicted vs actual)
        prediction_alerts = []
        for cat in categories:
            # Actual transactions in current week
            current_week = df[
                (df['date'] >= today - timedelta(days=6)) & (df['category'] == cat)
                ]['transactions'].sum()

            # 🔮 Simulated prediction for next week
            predicted_next_week = sum(random.randint(500, 1300) for _ in range(7))  # 7 days of predicted txns

            if current_week == 0:
                continue  # avoid divide by zero

            growth = ((predicted_next_week - current_week) / current_week) * 100
            message = (
                f"{cat} is expected to {'grow' if growth > 0 else 'drop'} "
                f"{abs(growth):.1f}% WoW ({current_week} → {predicted_next_week} txns)"
            )
            color = "success" if growth > 0 else "danger"
            prediction_alerts.append((abs(growth), dbc.Alert("🔮 " + message, color=color)))

        # Show top 3 largest predicted changes
        prediction_alerts.sort(reverse=True, key=lambda x: x[0])
        alerts.extend([alert for _, alert in prediction_alerts[:3]])

        return alerts