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


@router.post('/predict')
async def predict_category(request: Request):
    data = await request.json()
    req_categories = data['req_categories']

    # days = ['Today', '1 Day', '2 Days', '3 Days', '4 Days', '5 Days', '6 Days']
    # forecast = {day: [] for day in days}
    # for cat in categories:
    #     df = get_past_days_data_category(cat)
    #     df_amount = df.drop(columns=['transaction_count'])
    #     df_count = df.drop(columns=['transaction_amount'])
    #
    #     forecast_amounts = model_forecast('category_amount', df_amount)
    #     forecast_counts = model_forecast('category_count', df_count)
    #
    #     for day, amount, count in zip(days, forecast_amounts, forecast_counts):
    #         forecast[day].append({
    #                 'category': cat,
    #                 'transaction_count': amount,
    #                 'transaction_amount': count
    #             })
    # #
    forecast_data = {
        "Today": [
            {"category": "bank_transaction", "transaction_count": 12500, "transaction_amount": 8750000},
            {"category": "bill_payment", "transaction_count": 8200, "transaction_amount": 45600000},
            {"category": "education", "transaction_count": 15800, "transaction_amount": 12300000},
            {"category": "entertainment", "transaction_count": 22000, "transaction_amount": 67800000},
            {"category": "government", "transaction_count": 450, "transaction_amount": 2100000},
            {"category": "insurance", "transaction_count": 560, "transaction_amount": 3450000},
            {"category": "loan", "transaction_count": 1300, "transaction_amount": 15000000},
            {"category": "shopping", "transaction_count": 8900, "transaction_amount": 7200000},
            {"category": "topup", "transaction_count": 16800, "transaction_amount": 9500000},
        ],
        "1 Day After": [
            {"category": "bank_transaction", "transaction_count": 26000, "transaction_amount": 18000000},
            {"category": "bill_payment", "transaction_count": 16800, "transaction_amount": 89000000},
            {"category": "education", "transaction_count": 31000, "transaction_amount": 26000000},
            {"category": "entertainment", "transaction_count": 44000, "transaction_amount": 135000000},
            {"category": "government", "transaction_count": 920, "transaction_amount": 4250000},
            {"category": "insurance", "transaction_count": 1120, "transaction_amount": 6800000},
            {"category": "loan", "transaction_count": 2600, "transaction_amount": 32000000},
            {"category": "shopping", "transaction_count": 17800, "transaction_amount": 14500000},
            {"category": "topup", "transaction_count": 33600, "transaction_amount": 19000000},
        ],
        "2 Days After": [
            {"category": "bank_transaction", "transaction_count": 39000, "transaction_amount": 27500000},
            {"category": "bill_payment", "transaction_count": 24800, "transaction_amount": 134000000},
            {"category": "education", "transaction_count": 47000, "transaction_amount": 39500000},
            {"category": "entertainment", "transaction_count": 66000, "transaction_amount": 200000000},
            {"category": "government", "transaction_count": 1400, "transaction_amount": 6300000},
            {"category": "insurance", "transaction_count": 1680, "transaction_amount": 10200000},
            {"category": "loan", "transaction_count": 3900, "transaction_amount": 48000000},
            {"category": "shopping", "transaction_count": 26700, "transaction_amount": 21700000},
            {"category": "topup", "transaction_count": 50400, "transaction_amount": 28500000},
        ],
        "3 Days After": [
            {"category": "bank_transaction", "transaction_count": 39000, "transaction_amount": 27500000},
            {"category": "bill_payment", "transaction_count": 24800, "transaction_amount": 13400000},
            {"category": "education", "transaction_count": 47000, "transaction_amount": 3950000},
            {"category": "entertainment", "transaction_count": 66000, "transaction_amount": 20000000},
            {"category": "government", "transaction_count": 1400, "transaction_amount": 6300000},
            {"category": "insurance", "transaction_count": 1680, "transaction_amount": 10200000},
            {"category": "loan", "transaction_count": 3900, "transaction_amount": 48000000},
            {"category": "shopping", "transaction_count": 26700, "transaction_amount": 2170000},
            {"category": "topup", "transaction_count": 100400, "transaction_amount": 2500000},
        ],
        "4 Days After": [
            {"category": "bank_transaction", "transaction_count": 39000, "transaction_amount": 2750000},
            {"category": "bill_payment", "transaction_count": 24800, "transaction_amount": 134000000},
            {"category": "education", "transaction_count": 47000, "transaction_amount": 3950000},
            {"category": "entertainment", "transaction_count": 6600, "transaction_amount": 20000000},
            {"category": "government", "transaction_count": 1400, "transaction_amount": 6300000},
            {"category": "insurance", "transaction_count": 1680, "transaction_amount": 10200000},
            {"category": "loan", "transaction_count": 3900, "transaction_amount": 4800000},
            {"category": "shopping", "transaction_count": 26700, "transaction_amount": 21700000},
            {"category": "topup", "transaction_count": 100400, "transaction_amount": 2500000},
        ],
        "5 Days After": [
            {"category": "bank_transaction", "transaction_count": 39000, "transaction_amount": 2750000},
            {"category": "bill_payment", "transaction_count": 2480, "transaction_amount": 134000000},
            {"category": "education", "transaction_count": 47000, "transaction_amount": 39500000},
            {"category": "entertainment", "transaction_count": 66000, "transaction_amount": 20000000},
            {"category": "government", "transaction_count": 1400, "transaction_amount": 6300000},
            {"category": "insurance", "transaction_count": 1680, "transaction_amount": 10200000},
            {"category": "loan", "transaction_count": 3900, "transaction_amount": 4800000},
            {"category": "shopping", "transaction_count": 26700, "transaction_amount": 2170000},
            {"category": "topup", "transaction_count": 100400, "transaction_amount": 2500000},
        ],
        "6 Days After": [
            {"category": "bank_transaction", "transaction_count": 3900, "transaction_amount": 2750000},
            {"category": "bill_payment", "transaction_count": 24800, "transaction_amount": 13400000},
            {"category": "education", "transaction_count": 47000, "transaction_amount": 39500000},
            {"category": "entertainment", "transaction_count": 66000, "transaction_amount": 20000000},
            {"category": "government", "transaction_count": 1400, "transaction_amount": 6300000},
            {"category": "insurance", "transaction_count": 1680, "transaction_amount": 1020000},
            {"category": "loan", "transaction_count": 3900, "transaction_amount": 48000000},
            {"category": "shopping", "transaction_count": 26700, "transaction_amount": 21700000},
            {"category": "topup", "transaction_count": 100400, "transaction_amount": 2500000},
        ]
    }

    return forecast_data

