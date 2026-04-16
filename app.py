# ══════════════════════════════════════════════════════════════════════════════
#  app.py  —  Entry point. Run this file to start the dashboard.
#
#  Usage:
#    python app.py
#
#  File structure:
#    app.py        ← YOU ARE HERE (entry point — just runs the server)
#    server.py     ← Creates Dash app + Flask server
#    config.py     ← All constants, API keys, credentials, plan limits
#    data.py       ← Data fetching, signal engine, pattern detection, news
#    ml.py         ← XGBoost ML engine, backtesting, training
#    pages.py      ← All page layouts (landing, login, dashboard, pricing, etc.)
#    callbacks.py  ← All @app.callback functions + root layout + index_string
#    payment.py    ← PayPal subscription routes
# ══════════════════════════════════════════════════════════════════════════════

# Import order matters — server first, then modules that register on it
import payment                   # noqa: F401  registers Flask routes
import callbacks                 # noqa: F401  registers Dash callbacks + sets layout

if __name__ == "__main__":
    app.run(debug=False)
