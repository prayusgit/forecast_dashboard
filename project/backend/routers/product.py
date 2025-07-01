# Default Imports
from fastapi import APIRouter, Body
from typing import Dict

# Module Imports
from services.data_loader import get_past_days_data_product, get_past_days_prediction_product
from services.forecast import forecast_product
from services.model import load_model

router = APIRouter()

@router.get('/forecast/product-amount/{category}/{product}')
def forecast_category_amount(category: str, product: str):
    model_data = load_model('product_amount')
    model = model_data['model']
    category_target_mean = model_data['category_target_mean']
    product_target_mean = model_data['product_target_mean']
    global_mean = model_data['global_mean']

    aggregated_df = get_past_days_data_product(category, product)

    df_past_actual = aggregated_df[['transaction_date', 'transaction_amount']]
    df_past_actual['type'] = 'actual'

    df_past_forecast = get_past_days_prediction_product(category, product)
    df_past_forecast['type'] = 'forecast'

    df_future_forecast = forecast_product(category, product, model, aggregated_df, category_target_mean,
                                 product_target_mean, global_mean, num_days=7, target_col='transaction_amount')

    df_future_forecast['lower'] = df_future_forecast['transaction_amount'].apply(lambda x: x * 0.8)
    df_future_forecast['upper'] = df_future_forecast['transaction_amount'].apply(lambda x: x * 1.2)
    df_future_forecast['type'] = 'forecast'

    return {
        'past_data_actual': df_past_actual.to_dict(),
        'past_data_forecast': df_past_forecast.to_dict(),
        'future_data_forecast': df_future_forecast.to_dict()
    }


@router.post('/forecast')
def get_product_forecast(body: Dict = Body(...)):
    category = body.get('category')
    products = body.get('products')

    model_data = load_model('product_amount')
    model = model_data['model']
    category_target_mean = model_data['category_target_mean']
    product_target_mean = model_data['product_target_mean']
    global_mean = model_data['global_mean']

    forecast_list = []

    for prod in products:
        aggregated_df = get_past_days_data_product(category, prod)  # For past 30 days

        # 🔮 prediction for next week
        predicted_next_week = \
        forecast_product(category, prod, model, aggregated_df, category_target_mean, product_target_mean, global_mean,
                         num_days=7, target_col='transaction_amount')['transaction_amount'].sum()
        predicted_next_week = int(predicted_next_week)

        forecast_list.append({
                    'product': prod,
                    'transaction_amount': predicted_next_week})

    return {'data': forecast_list}
