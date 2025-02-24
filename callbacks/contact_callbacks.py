import pytz
from dash import Output, Input, State, callback
from models import schemas
from flask import request
from datetime import datetime
from database.connection import db
from config.config import contact_collection, timezone
from database.query import get_my_collection, add_contact_request
from functions.functions import email_checker


@callback(
    [
        Output("name-error", "children"),
        Output("email-error", "children"),
        Output("message-error", "children"),
    ],
    [Input("submit-form-btn", "n_clicks")],
    [
        State("name-input", "value"),
        State("email-input", "value"),
        State("message-input", "value"),
    ],
    prevent_initial_call=True,
)
def pre_validate_form(n_clicks, name, email, message):
    errors = ["", "", ""]

    if n_clicks > 0:
        if not name:
            errors[0] = "Proszę podać imię i nazwisko."
        if not email:
            errors[1] = "Proszę podać adres e-mail."
        if not message:
            errors[2] = "Proszę wpisać wiadomość."
        return errors
    return errors


@callback(
    [
        Output("submit-form-btn", "n_clicks"),
        Output("close-form-popup", "n_clicks"),
        Output("name-input", "value"),
        Output("email-input", "value"),
        Output("message-input", "value"),
        Output("contact-form-popup", "is_open"),
        Output("popup-form-header", "children"),
        Output("popup-form-body", "children"),
    ],
    [Input("submit-form-btn", "n_clicks"), Input("close-form-popup", "n_clicks")],
    [
        State("contact-form-popup", "is_open"),
        State("name-input", "value"),
        State("email-input", "value"),
        State("message-input", "value"),
    ],
    prevent_initial_call=True,
)
def send_user_request(
    n_clicks, close_clicks, is_open, user_name: str, user_email: str, user_message: str
):

    if close_clicks and not n_clicks > 0 and user_name and user_message:
        return (n_clicks, 0, user_name, "", user_message, not is_open, "", "")

    if close_clicks and not n_clicks > 0:
        return (n_clicks, 0, "", "", "", not is_open, "", "")

    if n_clicks > 0 and user_name and user_email and user_message:

        if len(user_name) > 100 or len(user_email) > 100 or len(user_message) > 5000:
            return (
                0,
                1,
                "",
                "",
                "",
                True,
                "Błąd",
                "Przekroczono maksymalną ilość znaków!",
            )

        if not email_checker(user_email):
            return (
                0,
                1,
                user_name,
                "",
                user_message,
                True,
                "Błąd",
                "Podany adres e-mail nie istnieje lub jest niepoprawny!",
            )

        contact_object = schemas.ContactRequest(
            requester_name=user_name,
            requester_email=user_email.lower(),
            requester_message=user_message,
            requester_timestamp=datetime.now(pytz.timezone(timezone)),
            requester_address=request.remote_addr,
        )
        is_request_added = add_contact_request(
            get_my_collection(db, contact_collection), contact_object
        )

        if is_request_added:
            return (
                0,
                1,
                "",
                "",
                "",
                True,
                "Informacja",
                "Twoja wiadomość została pomyślnie wysłana!",
            )
        else:
            return (
                0,
                1,
                "",
                "",
                "",
                True,
                "Błąd",
                "Wystąpił problem podczas wysyłania wiadomości!",
            )

    return (n_clicks, 0, user_name, user_email, user_message, is_open, "", "")
