# Default Imports
from fastapi import APIRouter, Request
from datetime import datetime, timedelta
import requests
import random

# Module Imports
from services.data_loader import get_past_days_data_category
from services.model import load_model

router = APIRouter()

@router.get('/transaction-alerts')
def get_alerts():
    prediction_alerts = []

    categories = requests.get('http://127.0.0.1:8000/api/info/categories').json()['categories']

    # model = load_model('category_count')

    for cat in categories:

        # Actual transactions in current week
        # df = get_past_days_data_category(cat)[['transaction_count', features]] # For past 30 days
        current_week = get_past_days_data_category(cat, past_days=7)['transaction_count'].sum()

        # 🔮 Simulated prediction for next week
        # predicted_next_week = model.predict(df)
        predicted_next_week = sum(random.randint(0, 20) for _ in range(7))  # 7 days of predicted txns

        if current_week == 0:
            continue  # avoid divide by zero

        growth = ((predicted_next_week - current_week) / current_week) * 100
        message = (
            f"{cat} is expected to {'grow' if growth > 0 else 'drop'} "
            f"{abs(growth):.1f}% WoW ({current_week} → {predicted_next_week} txns)"
        )
        color = "success" if growth > 0 else "danger"
        prediction_alerts.append((abs(growth), color, message))

    # Show top 3 largest predicted changes
    prediction_alerts.sort(reverse=True, key=lambda x: x[0])
    return {'alerts': prediction_alerts[:5]}


@router.post('/wow-growth')
async def get_wow_growth(request: Request):
    data = await request.json()
    req_categories = data['req_categories']

    # model = load_model('category_count')

    growth_list = []

    for cat in req_categories:

        # Actual transactions in current week
        # df = get_past_days_data_category(cat)[['transaction_count', features]] # For past 30 days
        current_week = get_past_days_data_category(cat, past_days=7)['transaction_amount'].sum()
        print(current_week)
        # 🔮 Simulated prediction for next week
        # predicted_next_week = model.predict(df)
        predicted_next_week = sum(random.randint(10000, 30000) for _ in range(7))  # 7 days of predicted txns

        if current_week == 0:
            continue  # avoid divide by zero

        growth = ((predicted_next_week - current_week) / current_week) * 100
        growth_list.append((cat, predicted_next_week, round(growth,2)))

    # Show top 3 largest predicted changes
    growth_list.sort(reverse=True, key=lambda x: abs(x[2]))
    return {'wow_growth_list': growth_list}