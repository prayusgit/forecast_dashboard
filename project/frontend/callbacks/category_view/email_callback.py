# Default Imports
from dash import dcc, html, Input, Output, State
import io
import smtplib
from email.message import EmailMessage
import pandas as pd
import plotly.io as pio
import io
import json


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'testforcoding32@gmail.com'
SENDER_PASSWORD = 'afqu nsss jfyi qmri'  # App password


def register_email_callback(app):
    # Callback to send email
    @app.callback(
        Output("category-email-modal", "is_open"),
        Output("category-email-modal-body", "children"),
        Input("category-email-send-btn", "n_clicks"),
        State("category-recipient-email", "value"),
        State("amount-forecast-graph", "figure"),
        State("volume-forecast-graph", "figure"),
        State("amount-growth-linechart", "figure"),
        State("volume-growth-linechart", "figure"),
        State("wow-table-data-store", "data"),
        prevent_initial_call=True
    )
    def send_report(n_clicks, recipient_email, fig_1, fig_2, fig_3, fig_4, table):
        df = pd.DataFrame(table)
        if not recipient_email:
            return True, "❌ Please enter a valid email address."

        try:
            fig_1 = pio.from_json(json.dumps(fig_1))
            fig_2 = pio.from_json(json.dumps(fig_2))
            fig_3 = pio.from_json(json.dumps(fig_3))
            fig_4 = pio.from_json(json.dumps(fig_4))
            figs = [fig_1, fig_2, fig_3, fig_4]
            send_email(figs, recipient_email, df)
            return True, f"✅ Email successfully sent to {recipient_email}!"
        except Exception as e:
            return True, f"❌ Error sending email: {str(e)}"

    # Close modal
    @app.callback(
        Output("category-email-modal", "is_open", allow_duplicate=True),
        Input("category-email-close-modal", "n_clicks"),
        State("category-email-modal", "is_open"),
        prevent_initial_call=True
    )
    def close_modal(n_clicks, is_open):
        return not is_open


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
