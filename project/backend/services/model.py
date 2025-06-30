# Module Imports
from .data_loader import get_past_days_data_category, get_past_days_data_product


model_category_amount = None
model_category_count = None
model_product_amount = None


def load_model(type):
    match type:
        case 'category_amount':
            global model_category_amount
            if model_category_amount is None:
                model_category_amount = 'model_category_amount' # joblib.load()
            return model_category_amount

        case 'category_count':
            global model_category_count
            if model_category_count is None:
                model_category_count = 'model_category_count'
            return model_category_count

        case 'product_amount':
            global model_product_amount
            if model_product_amount is None:
                model_product_amount = 'model_product_amount'
            return model_product_amount


def model_forecast(type, df):
    model = load_model(type)
    # forecast = model.predict(df)
    # return forecast
    pass
