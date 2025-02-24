import re
from dash import Output, Input, State, callback
from models import schemas
from database.connection import db
from config.config import server_list_collection
from database.query import (
    get_my_collection,
    is_server_in_database,
    add_server_to_database,
)
from functions.functions import address_checker
from functions.minecraft_server_checker import get_full_server_info


@callback(
    [
        Output("add-server-btn", "n_clicks"),
        Output("close-popup", "n_clicks"),
        Output("add-server-input", "value"),
        Output("server-added-popup", "is_open"),
        Output("popup-header", "children"),
        Output("popup-body", "children"),
    ],
    [Input("add-server-btn", "n_clicks"), Input("close-popup", "n_clicks")],
    [State("add-server-input", "value"), State("server-added-popup", "is_open")],
    prevent_initial_call=True,
)
def add_new_server(n_clicks, close_clicks, server_address: str, is_open):

    if close_clicks and not n_clicks > 0:
        return (0, 0, "", not is_open, "", "")

    if n_clicks > 0:
        if not server_address:
            return (0, 1, "", True, "Bład", "Wprowadź adres serwera Minecraft!")

        clean_server_address = re.sub(r"\s+", "", server_address).lower()

        if not address_checker(clean_server_address):
            return (0, 1, "", True, "Bład", "Wprowadzony adres jest niepoprawny!")

        is_server = is_server_in_database(
            get_my_collection(db, server_list_collection), clean_server_address
        )
        if is_server:
            return (
                0,
                1,
                "",
                True,
                "Bład",
                "Podany serwer został już dodany!",
            )

        full_server_info = get_full_server_info(clean_server_address)
        if not full_server_info:
            return (
                0,
                1,
                "",
                True,
                "Bład",
                "Serwer nie jest osiągalny pod podanym adresem!",
            )

        server_object = schemas.Server(
            server_address=clean_server_address,
            server_status=True,
            server_version=full_server_info[1],
            server_last_check_timestamp=full_server_info[0],
            server_last_online_timestamp=full_server_info[0],
            players_online=full_server_info[2],
            players_max=full_server_info[3],
        )
        is_server_added = add_server_to_database(
            get_my_collection(db, server_list_collection), server_object
        )

        if is_server_added:
            return (
                0,
                1,
                "",
                True,
                "Informacja",
                "Serwer został pomyślnie dodany!",
            )
        else:
            return (
                0,
                1,
                "",
                True,
                "Bład",
                "Błąd podczas dodawania serwera!",
            )

    return (0, 0, "", is_open, "", "")
