# Module Imports
from .data_loader import get_past_days_data_category, get_past_days_data_product
import pickle

model_category_amount = None
model_category_count = None
model_product_amount = None


def load_model(type):
    match type:
        case 'category_amount':
            global model_category_amount
            if model_category_amount is None:
                with open(r"E:/forecast_dashboard/modeling/ML/models/xgb_model_category_amount.pkl", "rb") as f:
                    model_category_amount = pickle.load(f)
            return model_category_amount

        case 'category_count':
            global model_category_count
            if model_category_count is None:
                with open(r"E:/forecast_dashboard/modeling/ML/models/xgb_model_category_count.pkl", "rb") as f:
                    model_category_count = pickle.load(f)
            return model_category_count

        case 'product_amount':
            global model_product_amount
            if model_product_amount is None:
                with open(r"E:/forecast_dashboard/modeling/ML/models/xgb_model_product_amount.pkl", "rb") as f:
                    model_product_amount = pickle.load(f)
            return model_product_amount


