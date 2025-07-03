from fastapi import APIRouter, Body
from typing import Dict
from llm_insight.llm_service import LLMService
from services.data_loader import get_past_days_data_category, get_past_days_prediction_category, get_past_days_data_product, get_past_days_prediction_product

router = APIRouter()

@router.post('/chart-insight-amount')
def chart_insight_volume(body: Dict = Body(...)):
    category = body.get('category')
    if not category:
        return {"error": "Category is required"}

    # Fetch actual and predicted data for the last 30 days
    actual_df = get_past_days_data_category(category)
    pred_df = get_past_days_prediction_category(category)

    # Prepare data for LLM insight (amount/volume)
    metrics = {
        "total_transactions": int(actual_df['transaction_amount'].count()),
        "total_amount": float(actual_df['transaction_amount'].sum()),
        "avg_transaction_amount": float(actual_df['transaction_amount'].mean()),
        "category": category
    }
    predictions = {
        "transaction_amount": float(pred_df['transaction_amount'].tail(7).sum()),
        "transaction_count": int(pred_df['transaction_amount'].tail(7).count())
    }
    actuals = {
        "transaction_amount": float(actual_df['transaction_amount'].tail(7).sum()),
        "transaction_count": int(actual_df['transaction_amount'].tail(7).count())
    }
    chart_data = {
        "metrics": metrics,
        "predictions": predictions,
        "actuals": actuals
    }

    llm_service = LLMService()
    user_types = ["executive", "marketing", "engineering", "non-tech"]
    insights = {}
    for user_type in user_types:
        insights[user_type] = llm_service.generate_insight_volume(user_type, chart_data)

    return {"insights": insights}

@router.post('/chart-insight-count')
def chart_insight_count(body: Dict = Body(...)):
    category = body.get('category')
    if not category:
        return {"error": "Category is required"}

    # Fetch actual and predicted data for the last 30 days
    actual_df = get_past_days_data_category(category)
    pred_df = get_past_days_prediction_category(category)

    # Prepare data for LLM insight (count/traffic)
    metrics = {
        "total_transactions": int(actual_df['transaction_count'].count()),
        "total_count": int(actual_df['transaction_count'].sum()),
        "avg_transaction_count": float(actual_df['transaction_count'].mean()),
        "category": category
    }
    predictions = {
        "transaction_count": int(pred_df['transaction_count'].tail(7).sum()),
    }
    actuals = {
        "transaction_count": int(actual_df['transaction_count'].tail(7).sum()),
    }
    chart_data = {
        "metrics": metrics,
        "predictions": predictions,
        "actuals": actuals
    }

    llm_service = LLMService()
    user_types = ["executive", "marketing", "engineering", "non-tech"]
    insights = {}
    for user_type in user_types:
        insights[user_type] = llm_service.generate_insight_count(user_type, chart_data)

    return {"insights": insights}

@router.post('/chart-insight-product')
def chart_insight_product(body: Dict = Body(...)):
    category = body.get('category')
    product = body.get('product')
    
    if not category:
        return {"error": "Category is required"}
    if not product:
        return {"error": "Product is required"}

    # Fetch actual and predicted data for the specific product
    actual_df = get_past_days_data_product(category, product)
    pred_df = get_past_days_prediction_product(category, product)

    # Prepare data for LLM insight (product-specific)
    metrics = {
        "total_transactions": int(actual_df['transaction_amount'].count()),
        "total_amount": float(actual_df['transaction_amount'].sum()),
        "avg_transaction_amount": float(actual_df['transaction_amount'].mean()),
        "category": category,
        "product": product
    }
    predictions = {
        "transaction_amount": float(pred_df['transaction_amount'].tail(7).sum()),
        "transaction_count": int(pred_df['transaction_amount'].tail(7).count())
    }
    actuals = {
        "transaction_amount": float(actual_df['transaction_amount'].tail(7).sum()),
        "transaction_count": int(actual_df['transaction_amount'].tail(7).count())
    }
    chart_data = {
        "metrics": metrics,
        "predictions": predictions,
        "actuals": actuals
    }

    llm_service = LLMService()
    user_types = ["executive", "marketing", "engineering", "non-tech"]
    insights = {}
    for user_type in user_types:
        insights[user_type] = llm_service.generate_insight_product(user_type, chart_data)

    return {"insights": insights}

