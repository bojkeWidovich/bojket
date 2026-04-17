import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True,
    update_title=None,
)
app.title = "Bojket"

server = app.server

# Load layout + all callbacks. Must be at the bottom (after `app` exists)
# so callbacks.py can do `from server import app` without circular issues.
import callbacks  # noqa: F401