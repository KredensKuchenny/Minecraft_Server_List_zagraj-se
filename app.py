import dash, threading
from dashseo import htmlify
from dash import Dash, html
import callbacks.navbar_callbacks
import callbacks.contact_callbacks
from components.footer import footer
from components.navbar import navbar
import callbacks.add_server_callbacks
import callbacks.server_list_callbacks
import dash_bootstrap_components as dbc
from config.config import production_mode, debug_mode
from functions.functions import list_updater, servers_updater


external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
]

app = Dash(
    __name__,
    pages_folder="pages",
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP] + external_css,
    assets_folder="assets",
    suppress_callback_exceptions=True,
)

app.layout = html.Div([navbar, dash.page_container, footer], className="page-view")

htmlify(app)

if production_mode:
    server = app.server
else:
    if __name__ == "__main__":
        background_process_1 = threading.Thread(target=list_updater, daemon=True)
        background_process_2 = threading.Thread(target=servers_updater, daemon=True)

        background_process_1.start()
        background_process_2.start()

        app.run(debug=debug_mode)
