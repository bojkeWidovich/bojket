# Bojket — VS Code Setup Guide

## File structure overview

```
trading-dashboard/
│
├── app.py          ← Entry point — run this to start the app
├── server.py       ← Creates the Dash app and Flask server
├── config.py       ← All settings: API keys, colours, plan limits, credentials
├── data.py         ← Price data, signal engine, pattern detection, news
├── ml.py           ← XGBoost ML model, backtesting, AI Lab
├── pages.py        ← Every page layout (landing, login, dashboard, pricing…)
├── callbacks.py    ← All interactive callbacks + root layout + CSS
├── payment.py      ← PayPal subscription routes
└── assets/         ← Static files (logo, images)
```

---

## Step 1 — Open the project folder in VS Code

1. Open **VS Code**.
2. Click **File → Open Folder…**
3. Navigate to the `trading-dashboard` folder and click **Open**.
4. The Explorer panel on the left now shows all 8 files.

---

## Step 2 — Install the Python extension (if not already installed)

1. Click the **Extensions** icon in the left sidebar (or press `Ctrl+Shift+X`).
2. Search for **Python** (by Microsoft).
3. Click **Install**.

---

## Step 3 — Install all required packages

1. Press `Ctrl+` `` ` `` to open the **integrated terminal**.
2. Run:
   ```
   pip3 install dash dash-bootstrap-components plotly pandas numpy yfinance ta requests scikit-learn xgboost
   ```
3. Wait for all packages to install (takes 1–2 minutes).

---

## Step 4 — Run the app

1. In the terminal, make sure you are inside the `trading-dashboard` folder:
   ```
   cd path/to/trading-dashboard
   ```
2. Run:
   ```
   python app.py
   ```
3. Open your browser and go to: **http://127.0.0.1:8050**

---

## Step 5 — Navigate the code in VS Code

### Quick jumps between files
- Click any filename in the **Explorer** panel on the left to open it.
- Press `Ctrl+P` and start typing a filename (e.g. `config`) to jump to it instantly.

### Jump to a specific function
- Press `Ctrl+Shift+O` inside any open file to see all functions — click to jump.
- Or press `Ctrl+G` and type a line number.

### Search across all files
- Press `Ctrl+Shift+F` to search for any variable or function across the entire project.

---

## Step 6 — What to edit where

| What you want to change | File to open |
|---|---|
| Your Groq API key | `config.py` → `GROQ_KEY` |
| PayPal keys | `config.py` → `PAYPAL_*` |
| Admin email / password | `config.py` → `ADMIN_EMAIL`, `ADMIN_PASSWORD` |
| Beta accounts | `config.py` → `BETA_ACCOUNTS` |
| Plan limits (features per tier) | `config.py` → `PLAN_LIMITS` |
| Colours (purple, bull green, etc.) | `config.py` → top of file |
| Landing page text / branding | `pages.py` → `landing_page()` function |
| Dashboard layout | `pages.py` → `dashboard_page()` function |
| Pricing page | `pages.py` → `pricing_page()` function |
| Buy button logic | `callbacks.py` → `handle_navigation()` function |
| Chart + signal update logic | `callbacks.py` → `update()` function (at the bottom) |
| ML training / backtesting | `ml.py` |
| Signal engine (BUY/SELL/WAIT logic) | `data.py` → `superintelligent_signal()` |
| TP / SL calculation | `data.py` → `get_levels()` |
| PayPal webhooks | `payment.py` |

---

## Step 7 — Making and saving changes

1. Open the file you want to edit.
2. Make your change.
3. Press `Ctrl+S` to save.
4. **Stop the running app** in the terminal with `Ctrl+C`.
5. Run `python app.py` again — changes take effect immediately.

> **Tip:** For small changes you can also press `Ctrl+S` and VS Code will auto-detect the change. If you run the app with `debug=True` (already set in `app.py`), Dash will reload automatically in the browser.

---

## Step 8 — Deploying / selling the app

When you want to publish or send this to someone:

1. **Remove or blank your API keys** in `config.py` before sharing (replace with `"your_key_here"` placeholders).
2. Send the entire `trading-dashboard/` folder as a zip file.
3. The buyer runs `python app.py` after installing packages.

### For server deployment (optional)
Replace `app.run(debug=True)` in `app.py` with:
```python
app.run(host="0.0.0.0", port=8050, debug=False)
```
Then run with Gunicorn:
```
gunicorn app:server -b 0.0.0.0:8050
```

---

## Quick reference — import chain

```
app.py
 ├── server.py        (creates app + server)
 ├── config.py        (constants, keys — no local imports)
 ├── data.py          (imports config)
 ├── ml.py            (imports config, lazy-imports data)
 ├── pages.py         (imports config)
 ├── callbacks.py     (imports server, config, data, ml, pages)
 └── payment.py       (imports server, config)
```

The import order in `app.py` guarantees no circular dependency issues.
