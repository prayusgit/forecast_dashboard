# Default Imports
from fastapi import APIRouter, Request
from datetime import datetime, timedelta
import requests
import random
import pandas as pd
import numpy as np


# Module Imports
from services.data_loader import get_past_days_data_category
from services.model import load_model, model_forecast

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

@router.get('/forecast/category-amount/{category}')
def forecast_category_amount(category: str):
    today = pd.Timestamp.today().normalize()
    df = get_past_days_data_category(category)

    df_past = df[['transaction_date', 'transaction_amount']]
    df_past['type'] = 'actual'

    future_days = pd.date_range(today, today + pd.Timedelta(days=6))

    forecast_base = df_past['transaction_amount'].iloc[-1]
    print(forecast_base)
    forecast_values = forecast_base + np.cumsum(np.random.randint(-5000, 5000, len(future_days)))
    # forecast_values = model_forecast('transaction_amount', df)

    lower_bound = forecast_values * 0.80
    upper_bound = forecast_values * 1.20

    df_future = pd.DataFrame({
        "transaction_date": future_days,
        "transaction_amount": forecast_values,
        "lower": lower_bound,
        "upper": upper_bound,
        "type": "forecast"
    })
    return {
        'past_data': df_past.to_dict(),
        'future_data': df_future.to_dict()
    }


@router.get('/forecast/category-count/{category}')
def forecast_category_volume(category: str):
    today = pd.Timestamp.today().normalize()
    df = get_past_days_data_category(category)

    df_past = df[['transaction_date', 'transaction_count']]
    df_past['type'] = 'actual'

    future_days = pd.date_range(today, today + pd.Timedelta(days=6))

    forecast_base = df_past['transaction_count'].iloc[-1]
    print(forecast_base)
    forecast_values = forecast_base + np.cumsum(np.random.randint(-3, 3, len(future_days)))
    # forecast_values = model_forecast('transaction_amount', df)

    lower_bound = forecast_values * 0.80
    upper_bound = forecast_values * 1.20

    df_future = pd.DataFrame({
        "transaction_date": future_days,
        "transaction_count": forecast_values,
        "lower": lower_bound,
        "upper": upper_bound,
        "type": "forecast"
    })
    return {
        'past_data': df_past.to_dict(),
        'future_data': df_future.to_dict()
    }


@router.post('/predict/category-count/{day_after}')
async def predict_category_count(day_after: int, request: Request):
    data = await request.json()
    pass

