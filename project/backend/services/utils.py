import datetime
from datetime import timedelta
import holidays
import pandas as pd

def is_festival_around_seven_days(festivals):
    today = datetime.today().date()
    pre_event_window = False
    post_event_window = False

    for i in range(8):  # today + next 7 days
        pre_date = today + timedelta(days=i)
        post_date = today - timedelta(days=i)
        if pre_date in holidays:
            pre_event_window = True
        if post_date in holidays:
            post_event_window = True

    return pre_event_window, post_event_window



# def update_forecast_csv(category_csv_path, product_csv_path):
#     today = datetime.today().date()
#     model_category_amount = load_model('category_amount')
#     model_category_count = load_model('category_count')
#     model_product_amount = load_model('product_amount')
#
#     # If CSV exists, read it. Otherwise, create empty DataFrame
#     if os.path.exists(category_csv_path):
#         df_category = pd.read_csv(category_csv_path, parse_dates=['transaction_date'])
#     else:
#         df_category = pd.DataFrame(columns=['transaction_date', 'category', 'transaction_amount', 'transaction_count'])
#
#     if os.path.exists(product_csv_path):
#         df_product = pd.read_csv(product_csv_path, parse_dates=['transaction_date'])
#     else:
#         df_product = pd.DataFrame(columns=['transaction_date', 'category', 'product', 'transaction_amount'])
#
#     aggregated_df_category = get_past_days_data_category(category)
#
#     for category, products in category_to_products.items():
#
#         # Check if today's forecast for the category exists
#         exists = ((df['date'] == pd.Timestamp(today)) & (df['category'] == category)).any()
#
#         if not exists:
#             # Call your custom forecast function that returns a single prediction for today
#             forecast_result_amount = forecast_category(
#                 category,
#                 model_category_amount['model'],
#                 aggregated_df_category,
#                 model_category_amount['category_target_mean'],
#                 model_category_amount['global_mean'],
#                 num_days=1,
#                 target_col='transaction_amount')['transaction_amount']
#
#             forecast_result_count = forecast_category(
#                 category,
#                 model_category_count['model'],
#                 aggregated_df_category,
#                 model_category_count['category_target_mean'],
#                 model_category_count['global_mean'],
#                 num_days=1,
#                 target_col='transaction_count')['transaction_count']
#
#             # Create new row
#             new_row = pd.DataFrame([{
#                 'transaction_date': today,
#                 'category': category,
#                 'transaction_amount': forecast_result_amount,
#                 'transaction_count': forecast_result_count
#             }])
#
#             # Append and save
#             df_category = pd.concat([df_category, new_row], ignore_index=True)
#             df_category.to_csv(category_csv_path, index=False)
#             print(f"✅ Forecast for '{category}' on {today} added.")
#         else:
#             print(f"✅ Forecast for '{category}' on {today} already exists.")
#
#             for product in products:
#                 aggregated_df_product = get_past_days_data_product(category, product)
#
#                 exists = ((aggregated_df_product['date'] == pd.Timestamp(today)) &
#                           (aggregated_df_product['category'] == category) &
#                           (aggregated_df_product['product'] == category)).any()
#                 if not exists:
#                     # Call your custom forecast function that returns a single prediction for today
#                     forecast_result_amount = forecast_product(
#                         category,
#                         model_product_amount['model'],
#                         aggregated_df_product,
#                         model_product_amount['category_target_mean'],
#                         model_product_amount['global_mean'],
#                         num_days=1,
#                         target_col='transaction_amount')['transaction_amount']
#
#
#                     # Create new row
#                     new_row = pd.DataFrame([{
#                         'transaction_date': today,
#                         'category': category,
#                         'product': product,
#                         'transaction_amount': forecast_result_amount,
#                     }])
#
#                     # Append and save
#                     df_product = pd.concat([df_product, new_row], ignore_index=True)
#                     df_product.to_csv(product_csv_path, index=False)
#                     print(f"✅ Forecast for '{category}' on {today} added.")
#                 else:
#                     print(f"✅ Forecast for '{category}' on {today} already exists.")
#
