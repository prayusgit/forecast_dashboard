# Default Imports
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output

# Module Imports
from layout.main_layout import create_main_layout
from callbacks.main_callback import register_callbacks


# External Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Transaction & Growth Forecast"

# Layout
app.layout = create_main_layout()

# Callback
register_callbacks(app)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
