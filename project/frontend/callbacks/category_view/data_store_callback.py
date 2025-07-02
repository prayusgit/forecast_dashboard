# Default Imports
from dash import Output, Input
import pandas as pd
import requests

def register_data_store_callback(app):
    @app.callback(
        Output('category-data-store', 'data'),
        [Input('multi-category-selection-dropdown', 'value'),
         Input('forecast-dropdown', 'value')]
    )
    def update_data_store(selected_categories, selected_forecast_day):
        response = requests.post('http://127.0.0.1:8000/api/category/predict/',
                                 json={'req_categories': selected_categories})
        data = response.json()[selected_forecast_day]

        df = pd.DataFrame(data)
        df = df[df['category'].isin(selected_categories)]

        return_data = {
            'selected_categories': selected_categories,
            'data': df.to_dict(),
            'selected_forecast_day': selected_forecast_day
        }
        return return_data



