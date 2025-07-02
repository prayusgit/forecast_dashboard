# Default Imports
import dash
import dash_bootstrap_components as dbc

# Module Imports
from layout.main_layout import create_main_layout
from callbacks.main_callback import register_callbacks


# External Bootstrap theme
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
        dbc.themes.BOOTSTRAP
    ],

    suppress_callback_exceptions=True,
)

# Layout
app.layout = create_main_layout()

# Callback
register_callbacks(app)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
