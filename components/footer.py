import pytz
from dash import html
from datetime import datetime
from config.config import brand_name, timezone

footer = html.Footer(
    className="footer-custom mt-auto py-3",
    children=html.Div(
        className="container text-center",
        children=html.Span(
            f"Wszelkie prawa zastrzeżone © {datetime.now(pytz.timezone(timezone)).year} {brand_name}"
        ),
    ),
)
