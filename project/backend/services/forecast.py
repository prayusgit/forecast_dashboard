# Default Imports
import pandas as pd
import numpy as np
from datetime import timedelta
import requests


features_category = [
    'category', 'is_event', 'is_holiday',
    'pre_event_window', 'post_event_window', 'day_of_week_sin',
    'day_of_week_cos', 'month_sin', 'month_cos', 'day_of_year_sin',
    'day_of_year_cos', 'lag_1', 'lag_7', 'lag_14', 'rolling_mean_7',
    'rolling_mean_14', 'event_type_disaster', 'event_type_festival',
    'event_type_none'
]


def forecast_category(category_name, model, aggregated_df, category_target_mean, global_mean, num_days=7,
                                  target_col='transaction_amount'):
    # Step 1: Filter past data for this category
    aggregated_df.sort_values('transaction_date', inplace=True)
    aggregated_df.reset_index(drop=True, inplace=True)

    # Step 2: Prepare future dates
    last_date = aggregated_df['transaction_date'].max()
    future_dates = pd.to_datetime([last_date + timedelta(days=i + 1) for i in range(num_days)])

    forecasts = []

    for forecast_date in future_dates:
        row = {}
        row['transaction_date'] = forecast_date

        # === Static Features ===
        row['category'] = category_target_mean.get(category_name, global_mean)

        data = requests.get(f'http://127.0.0.1:8000/api/calender/info/{forecast_date}').json()
        row['is_event'] = data.get('is_event', False)
        row['is_holiday'] = data.get('is_holiday', False)
        row['pre_event_window'] = data.get('pre_event_window', False)
        row['post_event_window'] = data.get('post_event_window', False)

        # === Cyclical Features ===
        dow = forecast_date.weekday()  # Monday=0
        row["day_of_week"] = row["transaction_date"].dayofweek
        row["day_of_week"] = ((row["day_of_week"] + 1) % 7) + 1
        row['day_of_week_sin'] = np.sin(2 * np.pi * dow / 7)
        row['day_of_week_cos'] = np.cos(2 * np.pi * dow / 7)

        month = forecast_date.month
        row['month_sin'] = np.sin(2 * np.pi * month / 12)
        row['month_cos'] = np.cos(2 * np.pi * month / 12)

        day_of_year = forecast_date.dayofyear
        row['day_of_year_sin'] = np.sin(2 * np.pi * day_of_year / 365)
        row['day_of_year_cos'] = np.cos(2 * np.pi * day_of_year / 365)

        # === One-hot Event Type ===
        row['event_type_festival'] = data.get('event_type', 'none') == 'festival'
        row['event_type_disaster'] = data.get('event_type', 'none') == 'disaster'
        row['event_type_none'] = data.get('event_type', 'none') == 'none'

        # === Lag and Rolling ===
        # Make sure to handle missing lag values (e.g. beginning of series)
        try:
            row['lag_1'] = aggregated_df.iloc[-1][target_col]
            row['lag_7'] = aggregated_df.iloc[-7][target_col] if len(aggregated_df) >= 7 else row['lag_1']
            row['lag_14'] = aggregated_df.iloc[-14][target_col] if len(aggregated_df) >= 14 else row['lag_7']
        except IndexError:
            row['lag_1'] = row['lag_7'] = row['lag_14'] = aggregated_df[target_col].mean()

        row['rolling_mean_7'] = aggregated_df[target_col].rolling(window=7).mean().iloc[-1] if len(aggregated_df) >= 7 else \
        aggregated_df[target_col].mean()
        row['rolling_mean_14'] = aggregated_df[target_col].rolling(window=14).mean().iloc[-1] if len(aggregated_df) >= 14 else \
        aggregated_df[target_col].mean()

        # Convert to DataFrame and predict
        X = pd.DataFrame([row])
        prediction = model.predict(X[features_category])[0]
        row[target_col] = prediction

        # Append to results
        forecasts.append(row)

        # Append to aggregated_df to maintain rolling window
        aggregated_df = pd.concat([aggregated_df, pd.DataFrame({
            'transaction_date': [forecast_date],
            target_col: [prediction]
        })], ignore_index=True)

    df = pd.DataFrame(forecasts)[['transaction_date', target_col]]
    df[target_col] = df[target_col].apply(lambda x: x if x >= 0 else 0)
    return df


features_product = [
       'product', 'category', 'is_event', 'is_holiday', 'pre_event_window',
       'post_event_window', 'day_of_week_sin', 'day_of_week_cos', 'month_sin',
       'month_cos', 'day_of_year_sin', 'day_of_year_cos', 'lag_1', 'lag_7',
       'lag_14', 'rolling_mean_7', 'rolling_mean_14', 'event_type_disaster',
       'event_type_festival', 'event_type_none'
       ]
def forecast_product(category_name, product_name, model, aggregated_df, category_target_mean,
                                 product_target_mean, global_mean, num_days=7, target_col='transaction_amount'):
    # Step 1: Filter past data for this category
    aggregated_df.sort_values('transaction_date', inplace=True)
    aggregated_df.reset_index(drop=True, inplace=True)

    # Step 2: Prepare future dates
    last_date = aggregated_df['transaction_date'].max()
    future_dates = pd.to_datetime([last_date + timedelta(days=i + 1) for i in range(num_days)])

    forecasts = []

    for forecast_date in future_dates:
        row = {}
        row['transaction_date'] = forecast_date

        # === Static Features ===
        row['category'] = category_target_mean.get(category_name, global_mean)
        row['product'] = product_target_mean.get(product_name, global_mean)

        data = requests.get(f'http://127.0.0.1:8000/api/calender/info/{forecast_date}').json()
        row['is_event'] = data.get('is_event', False)
        row['is_holiday'] = data.get('is_holiday', False)
        row['pre_event_window'] = data.get('pre_event_window', False)
        row['post_event_window'] = data.get('post_event_window', False)

        # === Cyclical Features ===
        dow = forecast_date.weekday()  # Monday=0
        row["day_of_week"] = row["transaction_date"].dayofweek
        row["day_of_week"] = ((row["day_of_week"] + 1) % 7) + 1
        row['day_of_week_sin'] = np.sin(2 * np.pi * dow / 7)
        row['day_of_week_cos'] = np.cos(2 * np.pi * dow / 7)

        month = forecast_date.month
        row['month_sin'] = np.sin(2 * np.pi * month / 12)
        row['month_cos'] = np.cos(2 * np.pi * month / 12)

        day_of_year = forecast_date.dayofyear
        row['day_of_year_sin'] = np.sin(2 * np.pi * day_of_year / 365)
        row['day_of_year_cos'] = np.cos(2 * np.pi * day_of_year / 365)

        # === One-hot Event Type ===
        row['event_type_festival'] = data.get('event_type', 'none') == 'festival'
        row['event_type_disaster'] = data.get('event_type', 'none') == 'disaster'
        row['event_type_none'] = data.get('event_type', 'none') == 'none'

        # === Lag and Rolling ===
        # Make sure to handle missing lag values (e.g. beginning of series)
        try:
            row['lag_1'] = aggregated_df.iloc[-1][target_col]
            row['lag_7'] = aggregated_df.iloc[-7][target_col] if len(aggregated_df) >= 7 else row['lag_1']
            row['lag_14'] = aggregated_df.iloc[-14][target_col] if len(aggregated_df) >= 14 else row['lag_7']
        except IndexError:
            row['lag_1'] = row['lag_7'] = row['lag_14'] = aggregated_df[target_col].mean()

        row['rolling_mean_7'] = aggregated_df[target_col].rolling(window=7).mean().iloc[-1] if len(aggregated_df) >= 7 else \
        aggregated_df[target_col].mean()
        row['rolling_mean_14'] = aggregated_df[target_col].rolling(window=14).mean().iloc[-1] if len(aggregated_df) >= 14 else \
        aggregated_df[target_col].mean()

        # Convert to DataFrame and predict
        X = pd.DataFrame([row])
        prediction = model.predict(X[features_product])[0]
        row[target_col] = prediction

        # Append to results
        forecasts.append(row)

        # Append to aggregated_df to maintain rolling window
        aggregated_df = pd.concat([aggregated_df, pd.DataFrame({
            'transaction_date': [forecast_date],
            target_col: [prediction]
        })], ignore_index=True)

    df = pd.DataFrame(forecasts)[['transaction_date', target_col]]
    df[target_col] = df[target_col].apply(lambda x: x if x >=0 else 0)
    return df