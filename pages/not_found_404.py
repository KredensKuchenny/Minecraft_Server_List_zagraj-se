import dash
from dash import html
import dash_bootstrap_components as dbc
from config.config import brand_name


dash.register_page(
    __name__,
    name="404 - Strona nie znaleziona",
    title=f"Strona nie znaleziona - {brand_name}",
)

layout = html.Div(
    className="main-container container",
    children=[
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
