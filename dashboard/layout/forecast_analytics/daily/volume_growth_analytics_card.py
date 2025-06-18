# Default Imports
import dash_bootstrap_components as dbc


# Module Imports
from components.daily.growth_analytics_linechart import  volume_growth_linechart
from components.daily.category_selection_dropdown import volume_category_selection_dropdown

def volume_growth_analytics_layout():
    return dbc.Card([
            dbc.CardHeader('Request Traffic Analytics'),
            dbc.CardBody([
                    volume_category_selection_dropdown,
                    volume_growth_linechart
                ])
            ])

