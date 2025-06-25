# Default Imports
from fastapi import APIRouter, Request
import pandas as pd
import numpy as np
import random

# Module Imports
from services.data_loader import get_past_days_data_product

router = APIRouter()

@router.get('/forecast/product-amount/{category}/{product}')
def forecast_category_amount(category: str, product: str):
    today = pd.Timestamp.today().normalize()
    df = get_past_days_data_product(category, product)

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

@router.post('/forecast')
async def get_product_forecast(request: Request):
    data = await request.json()
    category = data['category']
    products = data['products']

    # model = load_model('category_count')

    forecast_list = []

    for prod in products:

        # Actual transactions in current week
        # df = get_past_days_data_product(category, prod)[['transaction_count', features]] # For past 30 days
        # 🔮 Simulated prediction for next week
        # predicted_next_week = model.predict(df)

        predicted_next_week = sum(random.randint(10000, 30000) for _ in range(7))  # 7 days of predicted txns
        forecast_list.append({
                    'product': prod,
                    'transaction_amount': predicted_next_week})
    # Show top 3 largest predicted changes
    return {'data': forecast_list}
