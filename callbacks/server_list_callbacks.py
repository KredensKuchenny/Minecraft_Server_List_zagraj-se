from dash import Output, Input, State, callback, MATCH
import dash_bootstrap_components as dbc
from dash import dcc, html
from flask import request
from database.connection import db
from config.config import server_list_collection
from urllib.parse import parse_qs
from database.query import (
    get_my_collection,
    get_ranked_servers,
    get_document_count,
    add_vote_to_server,
    count_servers_by_address,
    search_ranked_servers,
)
from functions.functions import page_button_navigation, get_max_pages


@callback(
    [
        Output("server-list", "children"),
        Output("page-box", "children"),
        Output("prev-page-btn", "href"),
        Output("next-page-btn", "href"),
        Output("prev-page-btn", "disabled"),
        Output("next-page-btn", "disabled"),
        Output("page-changer-bar", "className"),
    ],
    [Input("search", "value"), Input("url", "search")],
)
def update_server_list(search_value: str, url_get):
    client_ip = request.remote_addr

    if search_value:
        max_elements_in_database = count_servers_by_address(
            get_my_collection(db, server_list_collection), search_value
        )
        max_pages = get_max_pages(max_elements_in_database)
    else:
        max_elements_in_database = get_document_count(
            get_my_collection(db, server_list_collection)
        )
        max_pages = get_max_pages(max_elements_in_database)

    page_number = 1
    if url_get:
        params = parse_qs(url_get.lstrip("?"))
        page_value = params.get("page", [None])[0]

        if page_value and page_value.isdigit():
            page_number = int(page_value)

            if page_number < 1 or page_number > max_pages:
                page_number = 1
        else:
            page_number = 1

    page_buttons = page_button_navigation(
        page_number, max_elements_in_database, max_pages
    )

    if search_value:
        servers = search_ranked_servers(
            get_my_collection(db, server_list_collection), client_ip, search_value
        )
    else:
        servers = get_ranked_servers(
            get_my_collection(db, server_list_collection), client_ip, page_number
        )

    return (
        [
            html.Div(
                className="server-item",
                children=[
                    html.Div(
                        className="server-info",
                        children=[
                            html.I(className="fas fa-server server-icon"),
                            html.Div(
                                children=[
                                    html.Div(
                                        server.server_address,
                                        className="server-name",
                                        id=f"copy-{server.server_address}",
                                    ),
                                    html.Div(
                                        className="server-players",
                                        children=[
                                            html.I(
                                                className="fa-solid fa-circle me-1",
                                                style={
                                                    "color": (
                                                        "#28a745"
                                                        if server.server_status
                                                        else "#dc3545"
                                                    )
                                                },
                                            ),
                                            f" {server.players_online} / {server.players_max} graczy",
                                        ],
                                    ),
                                    html.Div(
                                        className="server-version",
                                        children=[
                                            html.I(
                                                className="fas fa-cog me-1",
                                                style={"color": "silver"},
                                            ),
                                            f" Wersja: {server.server_version}",
                                        ],
                                    ),
                                    html.Div(
                                        id={
                                            "type": "votes-value",
                                            "index": server.server_address,
                                        },
                                        className="server-votes",
                                        children=[
                                            html.I(
                                                className="fa-solid fa-heart me-1",
                                                style={"color": "#f96fb9"},
                                            ),
                                            f" {server.server_votes}",
                                        ],
                                    ),
                                ]
                            ),
                        ],
                    ),
                    html.Div(
                        className="server-action",
                        children=[
                            html.Div(
                                className="server-vote",
                                children=[
                                    dbc.Button(
                                        id={
                                            "type": "vote-button",
                                            "index": server.server_address,
                                        },
                                        className="btn btn-vote",
                                        children=[
                                            html.I(className="fa-solid fa-heart")
                                        ],
                                        disabled=server.liked,
                                    )
                                ],
                            ),
                            html.Div(
                                className="server-address",
                                children=[
                                    dcc.Clipboard(
                                        className="btn btn-join",
                                        target_id=f"copy-{server.server_address}",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            )
            for server in servers
        ],
        page_number,
        f"/?page={page_buttons[0]}",
        f"/?page={ page_buttons[1]}",
        page_buttons[2],
        page_buttons[3],
        (
            "page-changer-bar-container display-none"
            if max_pages <= 1 or search_value
            else "page-changer-bar-container"
        ),
    )


@callback(
    [
        Output({"type": "vote-button", "index": MATCH}, "disabled"),
        Output({"type": "votes-value", "index": MATCH}, "children"),
    ],
    [
        Input({"type": "vote-button", "index": MATCH}, "n_clicks"),
    ],
    [
        State({"type": "vote-button", "index": MATCH}, "disabled"),
        State({"type": "votes-value", "index": MATCH}, "children"),
        State({"type": "vote-button", "index": MATCH}, "id"),
    ],
)
def update_like_status(n_clicks, vote_status, server_vote_counter, button_id):

    if n_clicks is None:
        return vote_status, server_vote_counter

    if n_clicks > 0:
        client_ip = request.remote_addr
        server_name = button_id["index"]

        vote_result = add_vote_to_server(
            get_my_collection(db, server_list_collection), client_ip, server_name
        )

        if vote_result:
            server_vote_counter[1] = f" {int(server_vote_counter[1].strip()) + 1}"
            return True, server_vote_counter

        else:
            return vote_status, server_vote_counter
