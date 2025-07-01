import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Button("Show Info", id="open-popup", color="primary"),

    dbc.Modal(
        [
            dbc.ModalHeader("Forecast Summary"),
            dbc.ModalBody("This dashboard displays predicted transaction volume and amount."),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-popup", className="ml-auto", n_clicks=0)
            ),
        ],
        id="popup-modal",
        is_open=False,
    )
])

@app.callback(
    Output("popup-modal", "is_open"),
    [Input("open-popup", "n_clicks"), Input("close-popup", "n_clicks")],
    [State("popup-modal", "is_open")]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

if __name__ == "__main__":
    app.run(debug=True)
