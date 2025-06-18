# Default Imports
import dash_bootstrap_components as dbc


# Module Imports
from components.daily.growth_analytics_linechart import amount_growth_linechart, volume_growth_linechart
from components.daily.category_selection_dropdown import amount_category_selection_dropdown

def amount_growth_analytics_layout():
    return dbc.Card([
            dbc.CardHeader('Growth Analytics'),
            dbc.CardBody([
                    amount_category_selection_dropdown,
                    amount_growth_linechart
                ])
            ])

