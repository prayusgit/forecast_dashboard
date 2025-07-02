# Default Imports
from fastapi import APIRouter, Request, Body
import requests
from typing import Dict


# Module Imports
from services.data_loader import get_past_days_data_category, get_past_days_prediction_category
from services.model import load_model
from services.forecast import forecast_category


router = APIRouter()

@router.get('/transaction-alerts')
def get_alerts():
    prediction_alerts = []

    categories = requests.get('http://127.0.0.1:8000/api/info/categories').json()['categories']
    model_data = load_model('category_count')
    model = model_data['model']
    category_target_mean = model_data['category_target_mean']
    global_mean = model_data['global_mean']

    for cat in categories:

        # Actual transactions in current week
        aggregated_df = get_past_days_data_category(cat) # For past 30 days

        current_week = aggregated_df.iloc[-7:]['transaction_count'].sum()

        # 🔮 Simulated prediction for next week
        predicted_next_week = forecast_category(cat, model, aggregated_df, category_target_mean, global_mean,
                                          num_days=7, target_col='transaction_count')['transaction_count'].sum()
        predicted_next_week = int(predicted_next_week)

        if current_week == 0:
            continue  # avoid divide by zero

        growth = ((predicted_next_week - current_week) / current_week) * 100
        message = (
            f"{cat} is expected to {'grow' if growth > 0 else 'drop'} "
            f"{abs(growth):.1f}% WoW ({current_week} → {predicted_next_week} txns)"
        )
        color = "success" if growth > 0 else "danger"
        prediction_alerts.append((abs(growth), color, message))

    # Show top 5 largest predicted changes
    prediction_alerts.sort(reverse=True, key=lambda x: x[0])
    return {'alerts': prediction_alerts[:5]}


@router.post('/wow-growth')
def get_wow_growth(body: Dict = Body(...)):

    req_categories = body.get('req_categories', [])

    model_data = load_model('category_amount')

    model = model_data['model']
    category_target_mean = model_data['category_target_mean']
    global_mean = model_data['global_mean']

    growth_list = []

    for cat in req_categories:

        # Actual transactions in current week
        # df = get_past_days_data_category(cat) # For past 30 days
        aggregated_df = get_past_days_data_category(cat)  # For past 30 days

        current_week = aggregated_df.iloc[-7:]['transaction_amount'].sum()
        # 🔮 prediction for next week
        predicted_next_week = forecast_category(cat, model, aggregated_df, category_target_mean, global_mean,
                                      num_days=7, target_col='transaction_count')['transaction_count'].sum()
        predicted_next_week = int(predicted_next_week)

        if current_week == 0:
            continue  # avoid divide by zero

        growth = ((predicted_next_week - current_week) / current_week) * 100
        growth_list.append((cat, predicted_next_week, round(growth,2)))

    # Show top 3 largest predicted changes
    growth_list.sort(reverse=True, key=lambda x: abs(x[2]))
    return {'wow_growth_list': growth_list}

@router.get('/forecast/category-amount/{category}')
def forecast_category_amount(category: str):
    model_data = load_model('category_amount')
    model = model_data['model']
    category_target_mean = model_data['category_target_mean']
    global_mean = model_data['global_mean']

    aggregated_df = get_past_days_data_category(category)

    df_past_actual = aggregated_df[['transaction_date', 'transaction_amount']]
    df_past_actual['type'] = 'actual'

    df_past_forecast = get_past_days_prediction_category(category)
    df_past_forecast['type'] = 'forecast'

    df_future_forecast = forecast_category(category, model, aggregated_df, category_target_mean, global_mean,
                                  num_days=7, target_col='transaction_amount')

    df_future_forecast['lower'] = df_future_forecast['transaction_amount'].apply(lambda x: x * 0.8)
    df_future_forecast['upper'] = df_future_forecast['transaction_amount'].apply(lambda x: x * 1.2)
    df_future_forecast['type'] = 'forecast'

    return {
        'past_data_actual': df_past_actual.to_dict(),
        'past_data_forecast': df_past_forecast.to_dict(),
        'future_data_forecast': df_future_forecast.to_dict()
    }


@router.get('/forecast/category-count/{category}')
def forecast_category_volume(category: str):
    model_data = load_model('category_count')
    model = model_data['model']
    category_target_mean = model_data['category_target_mean']
    global_mean = model_data['global_mean']

    aggregated_df = get_past_days_data_category(category)

    df_past_actual = aggregated_df[['transaction_date', 'transaction_count']]
    df_past_actual['type'] = 'actual'

    df_past_forecast = get_past_days_prediction_category(category)
    df_past_forecast['type'] = 'forecast'

    df_future_forecast = forecast_category(category, model, aggregated_df, category_target_mean, global_mean,
                                           num_days=7, target_col='transaction_count')

    df_future_forecast['lower'] = df_future_forecast['transaction_count'].apply(lambda x: x * 0.8)
    df_future_forecast['upper'] = df_future_forecast['transaction_count'].apply(lambda x: x * 1.2)
    df_future_forecast['type'] = 'forecast'

    return {
        'past_data_actual': df_past_actual.to_dict(),
        'past_data_forecast': df_past_forecast.to_dict(),
        'future_data_forecast': df_future_forecast.to_dict()
    }

@router.post('/predict')
def predict_category(body: Dict = Body(...)):
    req_categories = body.get('req_categories', [])

    amount_model_data = load_model('category_amount')
    amount_model = amount_model_data['model']
    category_amount_target_mean = amount_model_data['category_target_mean']
    amount_global_mean = amount_model_data['global_mean']

    count_model_data = load_model('category_count')
    count_model = count_model_data['model']
    category_count_target_mean = count_model_data['category_target_mean']
    count_global_mean = count_model_data['global_mean']

    days = ['Today', '1 Day After', '2 Days After', '3 Days After', '4 Days After', '5 Days After', '6 Days After']

    forecast = {day: [] for day in days}
    for cat in req_categories:
        aggregated_df = get_past_days_data_category(cat)

        forecast_amounts = forecast_category(cat, amount_model, aggregated_df, category_amount_target_mean, amount_global_mean,
                                                        num_days=7, target_col='transaction_amount')['transaction_amount']
        forecast_counts = forecast_category(cat, count_model, aggregated_df, category_count_target_mean, count_global_mean,
                                                        num_days=7, target_col='transaction_count')['transaction_count']

        for day, amount, count in zip(days, forecast_amounts, forecast_counts):
            forecast[day].append({
                    'category': cat,
                    'transaction_amount': int(amount),
                    'transaction_count': int(count)

                })

    return forecast
    # forecast_data = {
    #     "Today": [
    #         {"category": "bank_transaction", "transaction_count": 12500, "transaction_amount": 8750000},
    #         {"category": "bill_payment", "transaction_count": 8200, "transaction_amount": 45600000},
    #         {"category": "education", "transaction_count": 15800, "transaction_amount": 12300000},
    #         {"category": "entertainment", "transaction_count": 22000, "transaction_amount": 67800000},
    #         {"category": "government", "transaction_count": 450, "transaction_amount": 2100000},
    #         {"category": "insurance", "transaction_count": 560, "transaction_amount": 3450000},
    #         {"category": "loan", "transaction_count": 1300, "transaction_amount": 15000000},
    #         {"category": "shopping", "transaction_count": 8900, "transaction_amount": 7200000},
    #         {"category": "topup", "transaction_count": 16800, "transaction_amount": 9500000},
    #     ],
    #     "1 Day After": [
    #         {"category": "bank_transaction", "transaction_count": 26000, "transaction_amount": 18000000},
    #         {"category": "bill_payment", "transaction_count": 16800, "transaction_amount": 89000000},
    #         {"category": "education", "transaction_count": 31000, "transaction_amount": 26000000},
    #         {"category": "entertainment", "transaction_count": 44000, "transaction_amount": 135000000},
    #         {"category": "government", "transaction_count": 920, "transaction_amount": 4250000},
    #         {"category": "insurance", "transaction_count": 1120, "transaction_amount": 6800000},
    #         {"category": "loan", "transaction_count": 2600, "transaction_amount": 32000000},
    #         {"category": "shopping", "transaction_count": 17800, "transaction_amount": 14500000},
    #         {"category": "topup", "transaction_count": 33600, "transaction_amount": 19000000},
    #     ],
    #     "2 Days After": [
    #         {"category": "bank_transaction", "transaction_count": 39000, "transaction_amount": 27500000},
    #         {"category": "bill_payment", "transaction_count": 24800, "transaction_amount": 134000000},
    #         {"category": "education", "transaction_count": 47000, "transaction_amount": 39500000},
    #         {"category": "entertainment", "transaction_count": 66000, "transaction_amount": 200000000},
    #         {"category": "government", "transaction_count": 1400, "transaction_amount": 6300000},
    #         {"category": "insurance", "transaction_count": 1680, "transaction_amount": 10200000},
    #         {"category": "loan", "transaction_count": 3900, "transaction_amount": 48000000},
    #         {"category": "shopping", "transaction_count": 26700, "transaction_amount": 21700000},
    #         {"category": "topup", "transaction_count": 50400, "transaction_amount": 28500000},
    #     ],
    #     "3 Days After": [
    #         {"category": "bank_transaction", "transaction_count": 39000, "transaction_amount": 27500000},
    #         {"category": "bill_payment", "transaction_count": 24800, "transaction_amount": 13400000},
    #         {"category": "education", "transaction_count": 47000, "transaction_amount": 3950000},
    #         {"category": "entertainment", "transaction_count": 66000, "transaction_amount": 20000000},
    #         {"category": "government", "transaction_count": 1400, "transaction_amount": 6300000},
    #         {"category": "insurance", "transaction_count": 1680, "transaction_amount": 10200000},
    #         {"category": "loan", "transaction_count": 3900, "transaction_amount": 48000000},
    #         {"category": "shopping", "transaction_count": 26700, "transaction_amount": 2170000},
    #         {"category": "topup", "transaction_count": 100400, "transaction_amount": 2500000},
    #     ],
    #     "4 Days After": [
    #         {"category": "bank_transaction", "transaction_count": 39000, "transaction_amount": 2750000},
    #         {"category": "bill_payment", "transaction_count": 24800, "transaction_amount": 134000000},
    #         {"category": "education", "transaction_count": 47000, "transaction_amount": 3950000},
    #         {"category": "entertainment", "transaction_count": 6600, "transaction_amount": 20000000},
    #         {"category": "government", "transaction_count": 1400, "transaction_amount": 6300000},
    #         {"category": "insurance", "transaction_count": 1680, "transaction_amount": 10200000},
    #         {"category": "loan", "transaction_count": 3900, "transaction_amount": 4800000},
    #         {"category": "shopping", "transaction_count": 26700, "transaction_amount": 21700000},
    #         {"category": "topup", "transaction_count": 100400, "transaction_amount": 2500000},
    #     ],
    #     "5 Days After": [
    #         {"category": "bank_transaction", "transaction_count": 39000, "transaction_amount": 2750000},
    #         {"category": "bill_payment", "transaction_count": 2480, "transaction_amount": 134000000},
    #         {"category": "education", "transaction_count": 47000, "transaction_amount": 39500000},
    #         {"category": "entertainment", "transaction_count": 66000, "transaction_amount": 20000000},
    #         {"category": "government", "transaction_count": 1400, "transaction_amount": 6300000},
    #         {"category": "insurance", "transaction_count": 1680, "transaction_amount": 10200000},
    #         {"category": "loan", "transaction_count": 3900, "transaction_amount": 4800000},
    #         {"category": "shopping", "transaction_count": 26700, "transaction_amount": 2170000},
    #         {"category": "topup", "transaction_count": 100400, "transaction_amount": 2500000},
    #     ],
    #     "6 Days After": [
    #         {"category": "bank_transaction", "transaction_count": 3900, "transaction_amount": 2750000},
    #         {"category": "bill_payment", "transaction_count": 24800, "transaction_amount": 13400000},
    #         {"category": "education", "transaction_count": 47000, "transaction_amount": 39500000},
    #         {"category": "entertainment", "transaction_count": 66000, "transaction_amount": 20000000},
    #         {"category": "government", "transaction_count": 1400, "transaction_amount": 6300000},
    #         {"category": "insurance", "transaction_count": 1680, "transaction_amount": 1020000},
    #         {"category": "loan", "transaction_count": 3900, "transaction_amount": 48000000},
    #         {"category": "shopping", "transaction_count": 26700, "transaction_amount": 21700000},
    #         {"category": "topup", "transaction_count": 100400, "transaction_amount": 2500000},
    #     ]
    # }

    # return forecast_data

