import dash
from dash import dcc, html
from config.config import brand_name
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path="/add-server",
    name="Dodaj Serwer",
    title=f"Dodaj serwer na liście serwerów Minecraft - {brand_name}",
    description=f"Dodaj swój serwer Minecraft do listy na {brand_name}! Zdobądź nowych graczy i zwiększ popularność swojego serwera.",
    image="gamepad.png"
)

layout = html.Div(
    className="main-container container",
    children=[
        html.Meta(
            name="description",
            content=f"Dodaj swój serwer Minecraft do listy na {brand_name}! Zdobądź nowych graczy i zwiększ popularność swojego serwera.",
        ),
        html.Meta(
            name="keywords",
            content="dodaj serwer, serwery Minecraft, Minecraft Polska, lista serwerów, głosowanie na serwer, reklama serwera, promowanie serwera",
        ),
        html.H1(
            "Dodaj serwer Minecraft",
            className="text-center mb-4 page-title",
        ),
        html.Div(
            className="add-server-bar-container",
            children=[
                dcc.Input(
                    id="add-server-input",
                    type="text",
                    className="add-bar",
                    placeholder="Wpisz domenę lub adres IPv4...",
                    maxLength=100,
                ),
                dbc.Button(
                    ["Dodaj ", html.I(className="fa-solid fa-plus")],
                    className="btn btn-add",
                    id="add-server-btn",
                    n_clicks=0,
                ),
            ],
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("<undefined>", id="popup-header"),
                dbc.ModalBody("<undefined>", id="popup-body"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Zamknij",
                        id="close-popup",
                        class_name="btn",
                        n_clicks=0,
                    )
                ),
            ],
            class_name="popup-info",
            id="server-added-popup",
            is_open=False,
        ),
    ],
)
