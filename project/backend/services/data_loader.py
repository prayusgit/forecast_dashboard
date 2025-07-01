# Default Imports
import pandas as pd
from datetime import datetime, timedelta

_transaction_df = None  # cache in memory
_category_prediction_df = None
_product_prediction_df = None

########## Original data part
def load_transaction_data(refresh=False) -> pd.DataFrame:
    global _transaction_df

    if _transaction_df is None or refresh:
        df = pd.read_csv("../data/original_data/synthetic_data_v6.csv")  # or query DB
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], dayfirst=True, format='mixed')
        df['category'] = df['category'].astype(str)
        df['product'] = df['product'].astype(str)
        _transaction_df = df

    return _transaction_df.copy()


def get_past_days_data_category(category_name, past_days=30):
    today = datetime.today()
    start_date = today - timedelta(days=past_days + 1)
    end_date = today - timedelta(days=1)
    df = load_transaction_data()
    df = df[df['category'] == category_name]
    df = df[df['transaction_date'].between(start_date, end_date)]

    aggregated_df = df.groupby(["transaction_date"]).agg(
        transaction_count=("amount", "count"),
        transaction_amount=("amount", "sum")
    ).reset_index()

    # Reindex to include all date-category pairs
    aggregated_df = aggregated_df.set_index('transaction_date').asfreq('D', fill_value=0)

    # Reset index for further processing
    aggregated_df = aggregated_df.reset_index()
    return aggregated_df


def get_past_days_data_product(category_name, product_name, past_days=30):
    today = datetime.today()
    start_date = today - timedelta(days=past_days + 1)
    end_date = today - timedelta(days=1)
    df = load_transaction_data()
    df = df[(df['category'] == category_name) & (df['product'] == product_name)]
    df = df[df['transaction_date'].between(start_date, end_date)]

    aggregated_df = df.groupby(["transaction_date"]).agg(
        transaction_count=("amount", "count"),
        transaction_amount=("amount", "sum")
    ).reset_index()

    # Reindex to include all date-category pairs
    aggregated_df = aggregated_df.set_index('transaction_date').asfreq('D', fill_value=0)

    # Reset index for further processing
    aggregated_df = aggregated_df.reset_index()

    return aggregated_df


def get_past_days_data(past_days=30):
    today = datetime.today()
    start_date = today - timedelta(days=past_days + 1)
    end_date = today - timedelta(days=1)
    df = load_transaction_data()
    df = df[df['transaction_date'].between(start_date, end_date)]

    aggregated_df = df.groupby(["transaction_date"]).agg(
        transaction_count=("amount", "count"),
        transaction_amount=("amount", "sum")
    ).reset_index()

    # Reindex to include all date-category pairs
    aggregated_df = aggregated_df.set_index('transaction_date').asfreq('D', fill_value=0)

    # Reset index for further processing
    aggregated_df = aggregated_df.reset_index()
    return aggregated_df


############ Prediction data part
def load_category_prediction_data(refresh=False) -> pd.DataFrame:
    global _category_prediction_df

    if _category_prediction_df is None or refresh:
        df = pd.read_csv("../data/prediction_data/category_prediction_data_v6.csv")  # or query DB
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], dayfirst=True, format='mixed')
        df['category'] = df['category'].astype(str)
        _category_prediction_df = df
    return _category_prediction_df.copy()


def load_product_prediction_data(refresh=False) -> pd.DataFrame:
    global _product_prediction_df

    if _product_prediction_df is None or refresh:
        df = pd.read_csv("../data/prediction_data/product_prediction_data_v6.csv")  # or query DB
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], dayfirst=True, format='mixed')
        df['category'] = df['category'].astype(str)
        df['product'] = df['product'].astype(str)
        _product_prediction_df = df
    return _product_prediction_df.copy()


def get_past_days_prediction_category(category_name, past_days=30):
    today = datetime.today()
    start_date = today - timedelta(days=past_days + 1)
    end_date = today - timedelta(days=1)
    df = load_category_prediction_data()
    df = df[df['category'] == category_name]
    df = df[df['transaction_date'].between(start_date, end_date)]
    return df


def get_past_days_prediction_product(category_name, product_name, past_days=30):
    today = datetime.today()
    start_date = today - timedelta(days=past_days + 1)
    end_date = today - timedelta(days=1)
    df = load_product_prediction_data()
    df = df[(df['category'] == category_name) & (df['product'] == product_name)]
    df = df[df['transaction_date'].between(start_date, end_date)]
    return df

