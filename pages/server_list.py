import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from config.config import brand_name


dash.register_page(
    __name__,
    path="/",
    name="Strona Główna",
    title=f"Lista serwerów Minecraft - {brand_name}",
    description="Najlepsza lista serwerów Minecraft w Polsce! Przeglądaj serwery survival, skyblock, bedwars i wiele innych. Znajdź idealne miejsce do gry!",
    image="gamepad.png"
)


layout = html.Div(
    className="main-container container",
    children=[
        html.Meta(
            name="description",
            content="Najlepsza lista serwerów Minecraft w Polsce! Przeglądaj serwery survival, skyblock, bedwars i wiele innych. Znajdź idealne miejsce do gry!",
        ),
        html.Meta(
            name="keywords",
            content="Minecraft, serwery Minecraft, najlepsze serwery, lista serwerów, polskie serwery Minecraft, survival, skyblock, bedwars, tryby gry",
        ),
        dcc.Location(id="url"),
        html.H1(
            "Lista serwerów Minecraft",
            className="text-center mb-4 page-title",
        ),
        html.Div(
            className="search-bar-container",
            children=[
                dcc.Input(
                    id="search",
                    className="input-bar",
                    placeholder=" Wyszukaj serwer...",
                ),
            ],
        ),
        html.Div(id="server-list", className="server-list"),
        html.Div(
            id="page-changer-bar",
            className="page-changer-bar-container",
            children=[
                dbc.Button(
                    html.I(className="fa-solid fa-arrow-left"),
                    href="/",
                    className="btn btn-page",
                    id="prev-page-btn",
                    n_clicks=0,
                    disabled=False,
                ),
                html.Span("?", className="page-box", id="page-box"),
                dbc.Button(
                    html.I(className="fa-solid fa-arrow-right"),
                    href="/",
                    className="btn btn-page",
                    id="next-page-btn",
                    n_clicks=0,
                    disabled=False,
                ),
            ],
        ),
    ],
)
