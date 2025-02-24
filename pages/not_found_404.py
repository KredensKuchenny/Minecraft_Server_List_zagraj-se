import dash
from dash import html
import dash_bootstrap_components as dbc
from config.config import brand_name


dash.register_page(
    __name__,
    name="404 - Strona nie znaleziona",
    title=f"Strona nie znaleziona - {brand_name}",
    description="Najlepsza lista serwerów Minecraft w Polsce! Przeglądaj serwery survival, skyblock, bedwars i wiele innych. Znajdź idealne miejsce do gry!",
    image="gamepad.png",
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
        html.H1(
            "404 - Strona nie znaleziona",
            className="text-center mb-4 page-title",
        ),
        html.P(
            "Przepraszamy, ale strona, której szukasz, nie istnieje.",
            className="text-center mb-3 page-description",
        ),
    ],
)
