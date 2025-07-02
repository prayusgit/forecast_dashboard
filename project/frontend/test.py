
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.io as pio
import json
import io
import smtplib
from email.message import EmailMessage
import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    "Category": ["A", "B", "C"],
    "Transactions": [1000, 2000, 1500],
    "WoW Growth (%)": [5.2, -2.4, 3.1]
})

# Email credentials
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'testforcoding32@gmail.com'  # Your email
SENDER_PASSWORD = 'afqu nsss jfyi qmri'  # App password

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def generate_figures():
    fig1 = go.Figure(data=[go.Scatter(x=[2000, 2005, 2010, 2015, 2020], y=[1000, 2000, 3000, 2500, 4000])],
                    layout=go.Layout(title="Transaction Trend", xaxis_title="Year", yaxis_title="Amount"))
    fig2 = go.Figure(data=[go.Bar(x=["A", "B", "C"], y=[20, 14, 23])],
                    layout=go.Layout(title="Category Distribution"))
    return [fig1, fig2]

# Layout
app.layout = dbc.Container([
    html.H2("Forecast Graph & Data Viewer"),

    dcc.Graph(id="my-graph", figure=generate_figures()[0]),

    dash_table.DataTable(
        id='my-table',
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict("records"),
        style_cell={
            'textAlign': 'center',
            'padding': '10px',
            'font-family': 'Arial',
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{WoW Growth (%)} > 0',
                    'column_id': 'WoW Growth (%)'
                },
                'color': 'green',
                'fontWeight': 'bold'
            },
            {
                'if': {
                    'filter_query': '{WoW Growth (%) < 0}',
                    'column_id': 'WoW Growth (%)'
                },
                'color': 'red',
                'fontWeight': 'bold'
            },
        ],
        style_table={'overflowX': 'auto'},
        page_size=10
    ),

    dbc.Input(id="recipient-email", type="email", placeholder="Enter recipient email", className="mt-3 mb-2", debounce=True),

    dbc.Button("Send Email", id="send-btn", color="primary"),

    dcc.Loading(
        id="loading-spinner",
        type="circle",
        children=html.Div([
            dbc.Modal([
                dbc.ModalHeader("Email Status"),
                dbc.ModalBody(id="modal-body"),
                dbc.ModalFooter(dbc.Button("Close", id="close-modal", className="ms-auto"))
            ], id="email-modal", is_open=False)
        ])
    )
], fluid=True)

# Email sender function
def send_email(figs, receiver_email, df):
    msg = EmailMessage()
    msg["Subject"] = "Forecast Report: Graphs + Data"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    # HTML body with DataFrame
    table_html = df.to_html(index=False, border=1, justify='center')
    body_html = f"""
    <html>
    <body>
        <p>Hi,</p>
        <p>Attached are your forecast graphs. Below is the current data table:</p>
        {table_html}
        <p>Regards,<br>Dashboard Team</p>
    </body>
    </html>
    """
    msg.add_alternative(body_html, subtype="html")

    # Attach images
    for i, fig in enumerate(figs, 1):
        img_bytes = io.BytesIO()
        fig.write_image(img_bytes, format="png")
        img_bytes.seek(0)
        msg.add_attachment(img_bytes.read(), maintype="image", subtype="png", filename=f"graph_{i}.png")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

# Callback to send email
@app.callback(
    Output("email-modal", "is_open"),
    Output("modal-body", "children"),
    Input("send-btn", "n_clicks"),
    State("recipient-email", "value"),
    prevent_initial_call=True
)
def send_report(n_clicks, recipient_email):
    if not recipient_email:
        return True, "❌ Please enter a valid email address."

    try:
        figs = generate_figures()
        send_email(figs, recipient_email, df)
        return True, f"✅ Email successfully sent to {recipient_email}!"
    except Exception as e:
        return True, f"❌ Error sending email: {str(e)}"

# Close modal
@app.callback(
    Output("email-modal", "is_open", allow_duplicate=True),
    Input("close-modal", "n_clicks"),
    State("email-modal", "is_open"),
    prevent_initial_call=True
)
def close_modal(n_clicks, is_open):
    return not is_open

if __name__ == "__main__":
    app.run(debug=True)
