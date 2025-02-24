import dash_bootstrap_components as dbc
from config.config import brand_name

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand(f"{brand_name}", href="/", class_name="navbar-brand"),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(id="navbar-items", class_name="ms-auto"),
                id="navbar-collapse",
                navbar=True,
            ),
        ]
    ),
    dark=True,
    class_name="navbar-custom",
)
