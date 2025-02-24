from dash import Output, Input, State, callback
import dash_bootstrap_components as dbc
import dash


@callback(Output("navbar-items", "children"), Input("navbar-toggler", "n_clicks"))
def update_nav_items(n_clicks):
    return [
        dbc.NavItem(dbc.NavLink(page["name"], href=page["path"]))
        for page in dash.page_registry.values()
        if page["name"] != "404 - Strona nie znaleziona"
    ]


@callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
