# ══════════════════════════════════════════════════════════════════════════════
#  config.py  —  All constants, API keys, credentials, plan limits
#  No local imports. Safe to import from any other module.
# ══════════════════════════════════════════════════════════════════════════════

from datetime import datetime
import smtplib
import requests as http_req
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ── Colour palette ────────────────────────────────────────────────────────────
PURPLE      = "#9333EA"
PURPLE_LIGHT= "#A855F7"
PURPLE_GLOW = "rgba(147,51,234,0.25)"
BG_DARK     = "#060608"
BG_CARD     = "#0d0d0d"
BG_CARD2    = "#0f0e18"
BORDER      = "#1e1a2e"
BULL        = "#34d399"
BEAR        = "#f87171"
NEUTRAL     = "#c084fc"
TEXT_MAIN   = "#ffffff"
TEXT_DIM    = "#e2e0f0"
TEXT_MUTED  = "#9d9ab0"
MA50_COLOR  = "rgba(147,51,234,0.5)"
MA20_COLOR  = "rgba(192,132,252,0.45)"

# ── Admin credentials ─────────────────────────────────────────────────────────
ADMIN_EMAIL    = "admin@bojket.com"
ADMIN_PASSWORD = "bojket2025"

# ── Pre-made beta accounts (hand out one by one) ──────────────────────────────
# All get Veteran-level access, no admin panel, no onboarding flow.
BETA_ACCOUNTS = {
    "beta01@bojket.com": "Bk!Trade01",
    "beta02@bojket.com": "Bk!Trade02",
    "beta03@bojket.com": "Bk!Trade03",
    "beta04@bojket.com": "Bk!Trade04",
    "beta05@bojket.com": "Bk!Trade05",
    "beta06@bojket.com": "Bk!Trade06",
    "beta07@bojket.com": "Bk!Trade07",
    "beta08@bojket.com": "Bk!Trade08",
    "beta09@bojket.com": "Bk!Trade09",
    "beta10@bojket.com": "Bk!Trade10",
    "beta11@bojket.com": "Bk!Trade11",
    "beta12@bojket.com": "Bk!Trade12",
    "beta13@bojket.com": "Bk!Trade13",
    "beta14@bojket.com": "Bk!Trade14",
    "beta15@bojket.com": "Bk!Trade15",
}

# ── Email config ──────────────────────────────────────────────────────────────
EMAIL_SENDER   = "your_gmail@gmail.com"
EMAIL_PASSWORD = "your_16_char_app_password"
EMAIL_ENABLED  = False

PENDING_VERIFICATIONS = {}
VERIFIED_ACCOUNTS     = set()

# ── API keys ──────────────────────────────────────────────────────────────────
# Get your free key at: https://console.groq.com
GROQ_KEY = "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"

# ── PayPal payment config ─────────────────────────────────────────────────────
# Step 1: Create a PayPal Business account at https://paypal.com/business
# Step 2: Go to https://developer.paypal.com → My Apps & Credentials → Create App
# Step 3: Copy your Client ID and Secret below
# Step 4: Create 4 Subscription Plans and paste their P-xxxx IDs below
PAYPAL_CLIENT_ID       = "YOUR_PAYPAL_CLIENT_ID"
PAYPAL_CLIENT_SECRET   = "YOUR_PAYPAL_CLIENT_SECRET"
PAYPAL_PLAN_HUSTLER_MO = "P_YOUR_HUSTLER_MONTHLY_PLAN_ID"
PAYPAL_PLAN_HUSTLER_YR = "P_YOUR_HUSTLER_ANNUAL_PLAN_ID"
PAYPAL_PLAN_VETERAN_MO = "P_YOUR_VETERAN_MONTHLY_PLAN_ID"
PAYPAL_PLAN_VETERAN_YR = "P_YOUR_VETERAN_ANNUAL_PLAN_ID"
PAYPAL_SANDBOX         = True   # ← set to False when you go live

# ── Plan feature limits ───────────────────────────────────────────────────────
PLAN_LIMITS = {
    "admin":   {"max_patterns":8,"ai_msgs":99999,"htf":True, "divergence":True, "breakdown":True,"alerts":True,"journal":True},
    "veteran": {"max_patterns":8,"ai_msgs":99999,"htf":True, "divergence":True, "breakdown":True,"alerts":True,"journal":True},
    "hustler": {"max_patterns":4,"ai_msgs":7,    "htf":False,"divergence":False,"breakdown":False,"alerts":True,"journal":True},
    None:      {"max_patterns":0,"ai_msgs":0,    "htf":False,"divergence":False,"breakdown":False,"alerts":False,"journal":False},
}

# ── ML model file paths ───────────────────────────────────────────────────────
ML_MODEL_PATH  = "bojket_ml_model.pkl"
ML_SCALER_PATH = "bojket_ml_scaler.pkl"

FEATURE_NAMES = [
    "price_ema10","price_ema20","price_ema50",
    "ema10_ema20","ema20_ema50",
    "rsi","stoch_k","stoch_d","stoch_cross",
    "macd_hist","macd_hist_chg","macd_above_signal",
    "bb_position","vwap_pos",
    "vol_ratio","body_ratio","bull_candle",
    "ret_1","ret_5","ret_10","atr_ratio",
]


# ── AI system prompt ──────────────────────────────────────────────────────────
BOJKET_SYSTEM = """You are Bojket, an AI trading assistant built into the Bojket Trading Dashboard.
Your personality: Direct, honest, no fluff. Zero bullshit. You are a knowledgeable trading mentor.

You help with: candlestick patterns, RSI, MACD, support/resistance, Bollinger Bands, trends, entry/exit strategies, trading psychology, risk management, and all Bojket dashboard features.

You also have deep knowledge of the Bojket AI Lab and Machine Learning engine. Here is everything you know about it:

--- AI LAB & ML TRAINING ---
The AI Lab (the 🧠 AI Lab button in the topbar) is one of the most powerful features in Bojket. It contains two tools:

1. ML MODEL TRAINING
   What it is: An XGBoost machine learning model that learns from real historical market data.
   What it does: It analyzes 21 features per candle — EMA ratios, RSI, Stoch RSI, MACD histogram, Bollinger Band position, VWAP position, volume ratio, body ratio, candle direction, 1/5/10-candle returns, and ATR ratio — and learns which combinations predict winning trades.
   How it labels data: A trade is a WIN if price hits take profit (ATR x 1.4) before stop loss (ATR x 1.2). Otherwise it is a LOSS.
   How to train it: Open AI Lab → select your symbols (e.g. BTC-USD, ETH-USD) and timeframe (1h recommended) → click Train Model. It downloads 2 years of data, extracts features, and trains in the background. Takes 1-3 minutes.
   After training: The model saves to disk. Every signal on the dashboard now gets a ML boost — the model adjusts the bull/bear score based on what it learned. You will see a 🧠 ML BULL 72% badge on the chart. Feature importance shows which indicators matter most.
   Why it matters: Most retail traders use static rules written by someone else. Bojket's ML engine learns the specific patterns that have actually worked on the assets you trade, in the timeframe you trade. It replaces guesswork with statistical evidence.
   Retrain anytime: Market conditions change. Retrain every few weeks or when switching to a new asset class.

2. BACKTESTING ENGINE
   What it is: Runs Bojket's 10-factor signal engine over 2 years of historical data on any asset.
   What it shows: Total trades, win rate, average profit on wins, average loss on losses, profit factor, best/worst trade, and per-factor accuracy.
   How to use it: Open AI Lab → select a symbol and timeframe → click Run Backtest. Takes 30-60 seconds.
   Why it matters: Before trusting a strategy, you need to see how it performed historically. Backtesting is how professionals validate their edge. Most retail traders skip this step and wonder why they lose.

--- WHY THIS IS REVOLUTIONARY FOR MEMBERS ---
Most trading tools give every user the same static signals. Bojket's ML engine personalizes to you — your assets, your timeframe, your market conditions. It is a self-improving trading co-pilot that gets smarter the more you use it. Veteran traders pay thousands for backtesting tools alone. This is included in your Bojket membership.

Simple explanation for new users: "The ML training button teaches the AI your market. Pick which coins or stocks you trade, hit Train, and Bojket downloads 2 years of data and learns what patterns led to profitable trades. After that, every BUY/SELL signal gets boosted by what the model learned. It is like giving the signal engine a brain that has studied your specific market."

You do NOT discuss topics unrelated to trading or the Bojket dashboard.
Keep responses concise. Use short paragraphs or bullet points. Be encouraging but honest about risk."""

# ── Server-side user registry ─────────────────────────────────────────────────
# Persists for the lifetime of the server process (resets on restart).
REGISTERED_USERS = {}

def _register_user(email, plan, billing="monthly"):
    """Add a new user or update an existing user's plan/billing."""
    if not email or email.lower() == ADMIN_EMAIL.lower():
        return
    username = email.split("@")[0]
    now_str  = datetime.now().strftime("%d %b %Y  %H:%M")
    if email not in REGISTERED_USERS:
        REGISTERED_USERS[email] = {
            "email":      email,
            "username":   username,
            "plan":       plan,
            "billing":    billing,
            "joined":     now_str,
            "last_login": now_str,
            "last_login_iso": datetime.now().isoformat(),
            "trades":     [],
            "last_trade": "—",
        }
    else:
        REGISTERED_USERS[email]["plan"]    = plan
        REGISTERED_USERS[email]["billing"] = billing

def _mark_login(email):
    """Update last_login timestamp whenever a user signs in."""
    if not email or email.lower() == ADMIN_EMAIL.lower():
        return
    if email not in REGISTERED_USERS:
        return
    now = datetime.now()
    REGISTERED_USERS[email]["last_login"]     = now.strftime("%d %b %Y  %H:%M")
    REGISTERED_USERS[email]["last_login_iso"] = now.isoformat()

def send_verification_email(to_email, token):
    if not EMAIL_ENABLED: return True
    try:
        link = f"http://127.0.0.1:8050/verify?token={token}"
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Activate your Bojket account"
        msg["From"]    = EMAIL_SENDER
        msg["To"]      = to_email
        html_body = f"""
        <div style="background:#060608;padding:40px;font-family:Inter,sans-serif;max-width:520px;margin:0 auto">
          <div style="color:#9333EA;font-weight:800;font-size:1.4em;letter-spacing:4px;margin-bottom:8px">BOJKET</div>
          <div style="color:#9d9ab0;font-style:italic;font-size:0.85em;margin-bottom:32px">The future of trading.</div>
          <div style="color:#ffffff;font-size:1.1em;font-weight:600;margin-bottom:12px">Activate your account</div>
          <div style="color:#e2e0f0;font-size:0.9em;line-height:1.6;margin-bottom:28px">
            Click the button below to verify your email and activate your Bojket account.
          </div>
          <a href="{link}" style="background:#9333EA;color:white;padding:14px 28px;border-radius:10px;text-decoration:none;font-weight:600;font-size:0.9em;display:inline-block">
            Activate Account →
          </a>
        </div>"""
        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as srv:
            srv.login(EMAIL_SENDER, EMAIL_PASSWORD)
            srv.sendmail(EMAIL_SENDER, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Email error: {e}"); return False

# ── Groq AI call ──────────────────────────────────────────────────────────────
def call_bojket(messages, context=""):
    if not GROQ_KEY or GROQ_KEY.startswith("your_") or GROQ_KEY == "":
        return "⚠️ Bojket AI isn't connected yet. A Groq API key needs to be added — ask the admin."
    system_prompt = BOJKET_SYSTEM
    if context:
        system_prompt = BOJKET_SYSTEM + f"\n\n--- USER'S CURRENT DASHBOARD STATE ---\n{context}\n\nWhen the user asks about their current chart, signal, or trade, reference the state above. Be specific, not generic."
    try:
        r = http_req.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={"model":"llama-3.3-70b-versatile","max_tokens":800,
                  "messages":[{"role":"system","content":system_prompt}]+messages},
            timeout=25)
        if r.status_code == 401:
            return "⚠️ The Groq API key looks invalid or expired. It needs to be updated."
        if r.status_code == 429:
            return "I'm thinking really hard right now — give me a few seconds and try again."
        if r.status_code >= 500:
            return "Groq's servers are having a moment. Try again in a bit."
        data = r.json()
        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        return "Hmm, something went sideways. Try rephrasing or try again in a sec."
    except http_req.exceptions.Timeout:
        return "That took too long. Try a shorter question or try again in a moment."
    except http_req.exceptions.ConnectionError:
        return "Can't reach my brain right now. Check your connection or try again in a sec."
    except Exception:
        return "Something broke on my end. Try again in a moment."

# ── Asset / market data constants ─────────────────────────────────────────────
HIGHER_TF     = {"1m":"15m","5m":"1h","15m":"4h","30m":"4h","1h":"1d","2h":"1d","3h":"1d","4h":"1d","1d":"1wk"}
HIGHER_PERIOD = {"15m":"5d","1h":"1mo","4h":"3mo","1d":"1y","1wk":"2y"}

SYMBOLS = {
    "Crypto":      ["BTC-USD","ETH-USD","BNB-USD","SOL-USD","XRP-USD","DOGE-USD","ADA-USD","AVAX-USD","DOT-USD","MATIC-USD","LINK-USD","UNI-USD","ATOM-USD","LTC-USD","BCH-USD","NEAR-USD","APT-USD","OP-USD","ARB-USD","TON-USD","SUI-USD","TRX-USD","SHIB-USD","PEPE-USD"],
    "Commodities": ["GC=F","CL=F","SI=F","NG=F","HG=F","ZW=F","ZC=F","ZS=F"],
    "Indices":     ["NQ=F","ES=F","YM=F","RTY=F","DAX=F","NKD=F"],
    "Forex":       ["EURUSD=X","GBPUSD=X","USDJPY=X","AUDUSD=X","USDCAD=X","USDCHF=X","NZDUSD=X","EURGBP=X","EURJPY=X","GBPJPY=X"],
    "Stocks":      ["NVDA","AAPL","TSLA","AMZN","MSFT","META","GOOGL","NFLX","AMD","INTC","PYPL","CRM","UBER","SPOT","COIN","MSTR","JPM","BAC","GS","V","WMT"],
}

LABELS = {
    "BTC-USD":"Bitcoin","ETH-USD":"Ethereum","BNB-USD":"Binance Coin","SOL-USD":"Solana",
    "XRP-USD":"Ripple","DOGE-USD":"Dogecoin","ADA-USD":"Cardano","AVAX-USD":"Avalanche",
    "DOT-USD":"Polkadot","MATIC-USD":"Polygon","LINK-USD":"Chainlink","UNI-USD":"Uniswap",
    "ATOM-USD":"Cosmos","LTC-USD":"Litecoin","BCH-USD":"Bitcoin Cash","NEAR-USD":"NEAR Protocol",
    "APT-USD":"Aptos","OP-USD":"Optimism","ARB-USD":"Arbitrum","TON-USD":"Toncoin",
    "SUI-USD":"Sui","TRX-USD":"TRON","SHIB-USD":"Shiba Inu","PEPE-USD":"Pepe",
    "GC=F":"Gold","CL=F":"Crude Oil","SI=F":"Silver","NG=F":"Natural Gas",
    "HG=F":"Copper","ZW=F":"Wheat","ZC=F":"Corn","ZS=F":"Soybeans",
    "NQ=F":"Nasdaq Futures","ES=F":"S&P 500","YM=F":"Dow Jones","RTY=F":"Russell 2000",
    "DAX=F":"DAX Futures","NKD=F":"Nikkei 225",
    "EURUSD=X":"EUR / USD","GBPUSD=X":"GBP / USD","USDJPY=X":"USD / JPY",
    "AUDUSD=X":"AUD / USD","USDCAD=X":"USD / CAD","USDCHF=X":"USD / CHF",
    "NZDUSD=X":"NZD / USD","EURGBP=X":"EUR / GBP","EURJPY=X":"EUR / JPY","GBPJPY=X":"GBP / JPY",
    "NVDA":"Nvidia","AAPL":"Apple","TSLA":"Tesla","AMZN":"Amazon","MSFT":"Microsoft",
    "META":"Meta","GOOGL":"Google","NFLX":"Netflix","AMD":"AMD","INTC":"Intel",
    "PYPL":"PayPal","CRM":"Salesforce","UBER":"Uber","SPOT":"Spotify","COIN":"Coinbase",
    "MSTR":"MicroStrategy","JPM":"JPMorgan","BAC":"Bank of America","GS":"Goldman Sachs",
    "V":"Visa","WMT":"Walmart",
}

ASSET_ICONS = {
    "BTC-USD":"₿","ETH-USD":"Ξ","BNB-USD":"◈","SOL-USD":"◎","XRP-USD":"✕",
    "DOGE-USD":"Ð","ADA-USD":"₳","AVAX-USD":"▲","DOT-USD":"●","MATIC-USD":"◆",
    "LINK-USD":"⬡","UNI-USD":"◎","ATOM-USD":"⚛","LTC-USD":"Ł","BCH-USD":"₿",
    "NEAR-USD":"Ⓝ","APT-USD":"A","OP-USD":"O","ARB-USD":"A","TON-USD":"◎",
    "SUI-USD":"S","TRX-USD":"T","SHIB-USD":"◈","PEPE-USD":"◈",
    "GC=F":"Au","CL=F":"⛽","SI=F":"Ag","NG=F":"◈","HG=F":"Cu",
    "ZW=F":"◈","ZC=F":"◈","ZS=F":"◈",
    "NQ=F":"Nq","ES=F":"Sp","YM=F":"Dw","RTY=F":"Ru","DAX=F":"Dx","NKD=F":"Nk",
    "EURUSD=X":"€","GBPUSD=X":"£","USDJPY=X":"¥","AUDUSD=X":"A$","USDCAD=X":"C$",
    "USDCHF=X":"₣","NZDUSD=X":"N$","EURGBP=X":"€£","EURJPY=X":"€¥","GBPJPY=X":"£¥",
    "NVDA":"⬡","AAPL":"⌘","TSLA":"⚡","AMZN":"◻","MSFT":"⊞","META":"◈",
    "GOOGL":"G","NFLX":"N","AMD":"A","INTC":"I","PYPL":"P","CRM":"C",
    "UBER":"U","SPOT":"S","COIN":"₿","MSTR":"M","JPM":"J","BAC":"B",
    "GS":"G","V":"V","WMT":"W",
}

CATEGORY_ICONS = {"Crypto":"₿","Commodities":"◈","Indices":"≋","Forex":"⇄","Stocks":"⬡"}
ALL_OPTIONS    = [{"label":v,"value":k} for k,v in LABELS.items()]

# ── Candlestick pattern metadata ──────────────────────────────────────────────
ALL_PATTERNS = [
    ("Doji","neutral"),("Hammer","bullish"),("Inverted Hammer","bullish"),
    ("Hanging Man","bearish"),("Shooting Star","bearish"),
    ("Bullish Marubozu","bullish"),("Bearish Marubozu","bearish"),
    ("Spinning Top","neutral"),("High Wave","neutral"),
    ("Bullish Engulfing","bullish"),("Bearish Engulfing","bearish"),
    ("Bullish Harami","bullish"),("Bearish Harami","bearish"),
    ("Tweezer Tops","bearish"),("Tweezer Bottoms","bullish"),
    ("Dark Cloud Cover","bearish"),("Piercing Line","bullish"),
    ("Morning Star","bullish"),("Evening Star","bearish"),
    ("Three White Soldiers","bullish"),("Three Black Crows","bearish"),
    ("Three Inside Up","bullish"),("Three Inside Down","bearish"),
    ("Dragonfly Doji","bullish"),("Gravestone Doji","bearish"),
    ("Long Legged Doji","neutral"),("Belt Hold Bullish","bullish"),
    ("Belt Hold Bearish","bearish"),("Kicker Bullish","bullish"),
    ("Kicker Bearish","bearish"),("Three Outside Up","bullish"),
    ("Three Outside Down","bearish"),("On Neck","bearish"),
]

PAT_COLOR = {"bullish": BULL, "bearish": BEAR, "neutral": NEUTRAL}

PAT_ABBR = {
    "Doji":"DJ","Hammer":"HM","Inverted Hammer":"IH","Hanging Man":"HGM",
    "Shooting Star":"SS","Bullish Marubozu":"BMB","Bearish Marubozu":"BRB",
    "Spinning Top":"SPT","High Wave":"HWV","Bullish Engulfing":"BUE",
    "Bearish Engulfing":"BRE","Bullish Harami":"BUH","Bearish Harami":"BRH",
    "Tweezer Tops":"TWT","Tweezer Bottoms":"TWB","Dark Cloud Cover":"DCC",
    "Piercing Line":"PRL","Morning Star":"MRS","Evening Star":"EVS",
    "Three White Soldiers":"3WS","Three Black Crows":"3BC",
    "Three Inside Up":"3IU","Three Inside Down":"3ID",
    "Dragonfly Doji":"DFD","Gravestone Doji":"GVD","Long Legged Doji":"LLD",
    "Belt Hold Bullish":"BHB","Belt Hold Bearish":"BHR",
    "Kicker Bullish":"KCB","Kicker Bearish":"KCR",
    "Three Outside Up":"3OU","Three Outside Down":"3OD","On Neck":"ON",
}

SEN_EMOJI  = {"bullish":"📈","bearish":"📉","neutral":"↔️"}
SEN_LABEL  = {"bullish":"Uptrend signal","bearish":"Downtrend signal","neutral":"Sideways"}
MAX_IND    = 8

DESCS = {
    "Doji":"Market indecision — reversal likely soon.",
    "Hammer":"Buyers pushed price back up — bullish reversal.",
    "Inverted Hammer":"Buyers testing highs — possible upward move.",
    "Hanging Man":"Sellers may be entering after an uptrend.",
    "Shooting Star":"Buyers failed to hold highs — watch for drop.",
    "Bullish Marubozu":"Full bull candle — strong buying momentum.",
    "Bearish Marubozu":"Full bear candle — strong selling momentum.",
    "Spinning Top":"Neither side in control — wait for next candle.",
    "High Wave":"Extreme uncertainty — direction unclear.",
    "Bullish Engulfing":"Bulls took over the previous bear candle — strong buy.",
    "Bearish Engulfing":"Bears took over the previous bull candle — strong sell.",
    "Bullish Harami":"Small bull inside a big bear — reversal building.",
    "Bearish Harami":"Small bear inside a big bull — reversal building.",
    "Tweezer Tops":"Double rejection at highs — sellers defending.",
    "Tweezer Bottoms":"Double support at lows — buyers defending.",
    "Dark Cloud Cover":"Bears pushed deep into bull territory — caution.",
    "Piercing Line":"Bulls pushed deep into bear territory — buy signal.",
    "Morning Star":"3-candle bottom reversal — strong buy after downtrend.",
    "Evening Star":"3-candle top reversal — strong sell after uptrend.",
    "Three White Soldiers":"Three rising bull candles — powerful uptrend.",
    "Three Black Crows":"Three falling bear candles — powerful downtrend.",
    "Three Inside Up":"Bullish reversal confirmed — buy opportunity.",
    "Three Inside Down":"Bearish reversal confirmed — sell opportunity.",
    "Dragonfly Doji":"Lower prices rejected hard — bullish.",
    "Gravestone Doji":"Higher prices rejected hard — bearish.",
    "Long Legged Doji":"Massive uncertainty in both directions.",
    "Belt Hold Bullish":"Opened at low, closed near high — bull strength.",
    "Belt Hold Bearish":"Opened at high, closed near low — bear strength.",
    "Kicker Bullish":"Sudden gap up from bearish — very strong buy.",
    "Kicker Bearish":"Sudden gap down from bullish — very strong sell.",
    "Three Outside Up":"Bullish engulfing confirmed — strong buy.",
    "Three Outside Down":"Bearish engulfing confirmed — strong sell.",
    "On Neck":"Bearish continuation — sellers still in control.",
}

NEWS_SOURCES    = {"Crypto":["BTC-USD","ETH-USD","SOL-USD"],"Markets":["SPY","QQQ","GC=F"],"Commodities":["CL=F","SI=F"],"Forex":["EURUSD=X","GBPUSD=X"],"Tech":["NVDA","AAPL","TSLA","MSFT"]}
NEWS_CAT_ICONS  = {"Crypto":"₿","Markets":"📊","Commodities":"◈","Forex":"⇄","Tech":"⬡"}
NEWS_CAT_COLORS = {"Crypto":"#f7931a","Markets":"#34d399","Commodities":"#facc15","Forex":"#60a5fa","Tech":"#a78bfa"}

# ── Device session tracking (max 2 devices per account) ──────────────────────
ACTIVE_SESSIONS = {}  # {email: set of session_ids}
MAX_DEVICES = 2

def register_session(email, session_id):
    """Register a new session. Returns True if allowed, False if device limit reached."""
    if not email: return True
    if email not in ACTIVE_SESSIONS:
        ACTIVE_SESSIONS[email] = set()
    if session_id in ACTIVE_SESSIONS[email]: return True
    if len(ACTIVE_SESSIONS[email]) >= MAX_DEVICES: return False
    ACTIVE_SESSIONS[email].add(session_id)
    return True

def unregister_session(email, session_id):
    """Remove a session when user signs out."""
    if email and email in ACTIVE_SESSIONS:
        ACTIVE_SESSIONS[email].discard(session_id)
