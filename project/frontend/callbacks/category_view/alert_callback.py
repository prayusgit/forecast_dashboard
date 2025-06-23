# Default Imports
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input
import pandas as pd
from datetime import datetime, timedelta
import random

# Sample data generation for transactions
categories = ['Ncell Topup', 'Electricity Bill', 'Khanepani Bill', 'TV Recharge', 'Internet Payment']
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

# Define a list of upcoming Nepali festivals (example only)
festivals = {
    "Asar 15": datetime(2025, 6, 30).date(),
    "Eid al-Adha": datetime(2025, 6, 25).date(),
    "Teej": datetime(2025, 8, 28).date()
}


def register_alert_callback(app):
    @app.callback(
        Output('alert-output', 'children'),
        Input('alert-output', 'id')  # Trigger on page load
    )
    def generate_alerts(_):
        alerts = []
        now = today

        # 1. Festival Alerts
        for fest_name, fest_date in festivals.items():
            days_diff = (fest_date - now).days
            if 0 <= days_diff <= 7:
                alerts.append(
                    dbc.Alert(f"✨ {fest_name} is in {days_diff} day(s). Expect transactional spike!", color="info")
                )

        # 2. WoW Alerts
        wow_alerts = []
        for cat in categories:
            current_week = df[(df['date'] >= today - timedelta(days=6)) & (df['category'] == cat)].transactions.sum()
            prev_week = df[(df['date'] < today - timedelta(days=6)) & (df['category'] == cat)].transactions.sum()
            if prev_week == 0:
                continue  # Avoid division by zero
            growth = ((current_week - prev_week) / prev_week) * 100
            message = f"{cat} {'grew' if growth > 0 else 'dropped'} {abs(growth):.1f}% WoW ({prev_week} → {current_week} txns)"
            color = "success" if growth > 0 else "danger"
            wow_alerts.append((abs(growth), dbc.Alert("\U0001F4C8 " + message, color=color)))

        # Show top 3 WoW changes
        wow_alerts.sort(reverse=True, key=lambda x: x[0])
        alerts.extend([alert for _, alert in wow_alerts[:3]])

        return alerts