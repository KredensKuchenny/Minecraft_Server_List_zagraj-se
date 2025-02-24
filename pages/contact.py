import dash
from dash import dcc, html
from config.config import brand_name
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path="/contact",
    name="Kontakt",
    title=f"Kontakt z listą serwerów Minecraft - {brand_name}",
    description=f"Skontaktuj się z nami w sprawie listy serwerów Minecraft na {brand_name}. Masz pytania lub chcesz zgłosić serwer? Napisz do nas!",
)

layout = html.Div(
    className="main-container container",
    children=[
        html.Meta(
            name="description",
            content=f"Skontaktuj się z nami w sprawie listy serwerów Minecraft na {brand_name}. Masz pytania lub chcesz zgłosić serwer? Napisz do nas!",
        ),
        html.Meta(
            name="keywords",
            content=f"kontakt, {brand_name}, lista serwerów Minecraft, pomoc, wsparcie, zgłoszenie serwera",
        ),
        html.H1(
            "Kontakt z nami",
            className="text-center mb-4 page-title",
        ),
        html.P(
            "Masz pytania lub potrzebujesz pomocy? Skontaktuj się z nami, wypełniając formularz poniżej.",
            className="text-center mb-3 page-description",
        ),
        html.Div(
            className="contact-form-container",
            children=[
                dbc.Form(
                    children=[
                        dbc.CardGroup(
                            [
                                dbc.Label(
                                    "Imię i nazwisko",
                                    html_for="name-input",
                                    class_name="mt-3 form-label",
                                ),
                                dcc.Input(
                                    id="name-input",
                                    type="text",
                                    className="input-bar",
                                    placeholder="Wpisz swoje imię i nazwisko",
                                ),
                                html.Div(id="name-error", className="text-danger mt-1"),
                            ]
                        ),
                        dbc.CardGroup(
                            [
                                dbc.Label(
                                    "Adres e-mail",
                                    html_for="email-input",
                                    class_name="mt-4 form-label",
                                ),
                                dcc.Input(
                                    id="email-input",
                                    type="email",
                                    className="input-bar",
                                    placeholder="Wpisz swój adres e-mail",
                                ),
                                html.Div(
                                    id="email-error", className="text-danger mt-1"
                                ),
                            ]
                        ),
                        dbc.CardGroup(
                            [
                                dbc.Label(
                                    "Wiadomość",
                                    html_for="message-input",
                                    class_name="mt-4 form-label",
                                ),
                                dcc.Textarea(
                                    id="message-input",
                                    className="input-bar",
                                    placeholder="Wpisz swoją wiadomość",
                                    rows=4,
                                ),
                                html.Div(
                                    id="message-error", className="text-danger mt-1"
                                ),
                            ]
                        ),
                        dbc.Button(
                            "Prześlij formularz",
                            color="primary",
                            class_name="btn-add mt-4 mx-auto",
                            id="submit-form-btn",
                            n_clicks=0,
                        ),
                    ]
                )
            ],
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("<undefined>", id="popup-form-header"),
                dbc.ModalBody("<undefined>", id="popup-form-body"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Zamknij",
                        id="close-form-popup",
                        class_name="btn",
                        n_clicks=0,
                    )
                ),
            ],
            class_name="popup-info",
            id="contact-form-popup",
            is_open=False,
        ),
    ],
)
