# ══════════════════════════════════════════════════════════════════════════════
#  server.py  —  Creates the Dash app and Flask server
#  All other modules import `app` and `server` from here.
#  This file has ZERO local imports — it is the foundation.
# ══════════════════════════════════════════════════════════════════════════════

import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True,
    update_title=None,
)
app.title = "Bojket"

# Flask server — used for payment routes and Gunicorn deployment
server = app.server
