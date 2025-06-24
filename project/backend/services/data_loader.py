import pandas as pd
from datetime import datetime, timedelta

_transaction_df = None  # cache in memory


def load_transaction_data(refresh=False) -> pd.DataFrame:
    global _transaction_df

    if _transaction_df is None or refresh:
        df = pd.read_csv("../data/synthetic_data_v3.csv")  # or query DB
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], dayfirst=True)
        df['category'] = df['category'].astype(str)
        df['product'] = df['product'].astype(str)
        _transaction_df = df

    return _transaction_df.copy()


# def get_get_transaction_summary(start_date: datetime, end_date: datetime, group_by='category'):
#     df = load_transaction_data()
#     df = df[df['transaction_date'].between(start_date, end_date)]
#     summary = df.groupby(group_by).agg(
#         transaction_count=('amount', 'count'),
#         total_amount=('amount', 'sum')
#     ).reset_index()
#     return summary


def get_past_days_data_category(category_name, past_days=30):
    today = datetime.today()
    start_date = today - timedelta(days=past_days+1)
    end_date = today - timedelta(days=1)
    df = load_transaction_data()
    df = df[df['transaction_date'].between(start_date, end_date)]
    df = df[df['category'] == category_name]
    summary = df.groupby(["transaction_date"]).agg(
        transaction_count=("amount", "count"),
        transaction_amount=("amount", "sum")
    ).reset_index()
    return summary


def get_past_days_data_product(product_name, past_days=30):
    today = datetime.today()
    start_date = today - timedelta(days=past_days+1)
    end_date = today - timedelta(days=1)
    df = load_transaction_data()
    df = df[df['transaction_date'].between(start_date, end_date)]
    df = df[df['product'] == product_name]
    summary = df.groupby(["transaction_date"]).agg(
        transaction_count=("amount", "count"),
        transaction_amount=("amount", "sum")
    ).reset_index()
    return summary

def get_past_days_data(past_days=30):
    today = datetime.today()
    start_date = today - timedelta(days=past_days+1)
    end_date = today - timedelta(days=1)
    df = load_transaction_data()
    df = df[df['transaction_date'].between(start_date, end_date)]
    summary = df.groupby(["transaction_date"]).agg(
        transaction_count=("amount", "count"),
        transaction_amount=("amount", "sum")
    ).reset_index()
    return summary

