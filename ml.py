# ══════════════════════════════════════════════════════════════════════════════
#  ml.py  —  XGBoost ML engine: training, prediction, backtesting, UI widgets
# ══════════════════════════════════════════════════════════════════════════════

import pickle
import threading
import numpy as np
import ta
from datetime import datetime
from dash import html
import plotly.graph_objects as go

# Graceful ML imports
try:
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

try:
    import xgboost as xgb
    HAS_XGB = True
except Exception:
    HAS_XGB = False

from config import (
    ML_MODEL_PATH, ML_SCALER_PATH, FEATURE_NAMES,
    BULL, BEAR, NEUTRAL, TEXT_MAIN, TEXT_DIM, TEXT_MUTED,
    BORDER, PURPLE, PLAN_LIMITS,
)

# ML state lives in ml.py so data.py can access via `import ml; ml._ML_MODEL`
_ML_LOCK   = threading.Lock()
_ML_STATE  = {
    "status":      "idle",
    "progress":    0,
    "message":     "Model not trained yet. Open AI Lab to train.",
    "accuracy":    None,
    "n_samples":   0,
    "trained_at":  None,
    "error":       None,
    "feat_imp":    None,
}
_ML_MODEL  = None
_ML_SCALER = None

_BT_LOCK  = threading.Lock()
_BT_STATE = {
    "status":  "idle",
    "progress": 0,
    "message": "",
    "results": None,
}

def _get_fetch_data():
    from data import fetch_data
    return fetch_data


# ══════════════════════════════════════════════════════════════════════════════
#  ML ENGINE — LEVEL 1 (BACKTESTING) + LEVEL 2 (XGBOOST)
# ══════════════════════════════════════════════════════════════════════════════

def extract_features(df):
    """Extract 21 numeric features from an OHLCV slice. Returns list or None."""
    if df is None or len(df) < 52:
        return None
    try:
        cl = df['close']
        last = cl.iloc[-1]
        if last == 0: return None

        e10 = cl.ewm(span=10, adjust=False).mean().iloc[-1]
        e20 = cl.ewm(span=20, adjust=False).mean().iloc[-1]
        e50 = cl.ewm(span=50, adjust=False).mean().iloc[-1]

        rsi_val = ta.momentum.RSIIndicator(cl, 14).rsi().iloc[-1]

        sk, sd = get_stoch_rsi(df)
        if sk is None: sk, sd = 0.5, 0.5

        m   = ta.trend.MACD(cl)
        mh  = m.macd_diff().iloc[-1]
        mhp = m.macd_diff().iloc[-2] if len(df) > 2 else mh
        mab = 1.0 if m.macd().iloc[-1] > m.macd_signal().iloc[-1] else 0.0

        bb_mid = cl.rolling(20).mean().iloc[-1]
        bb_std = cl.rolling(20).std().iloc[-1]
        bb_pos = (last - bb_mid) / (2 * bb_std + 1e-10)

        vwap_s = get_vwap_series(df)
        vwap_pos = (last / vwap_s.iloc[-1] - 1) if vwap_s is not None else 0.0

        vol_ratio = 1.0
        if 'volume' in df.columns:
            avg_v = df['volume'].iloc[-10:-1].mean()
            if avg_v > 0:
                vol_ratio = df['volume'].iloc[-1] / avg_v

        body = abs(df['close'].iloc[-1] - df['open'].iloc[-1])
        rng  = df['high'].iloc[-1] - df['low'].iloc[-1]
        body_ratio = body / (rng + 1e-10)
        bull_candle = 1.0 if df['close'].iloc[-1] > df['open'].iloc[-1] else 0.0

        ret1  = cl.pct_change(1).iloc[-1]
        ret5  = cl.pct_change(5).iloc[-1]
        ret10 = cl.pct_change(10).iloc[-1]

        atr_val = get_atr(df) or 0
        atr_ratio = atr_val / (last + 1e-10)

        feats = [
            last / (e10 + 1e-10) - 1,
            last / (e20 + 1e-10) - 1,
            last / (e50 + 1e-10) - 1,
            e10  / (e20 + 1e-10) - 1,
            e20  / (e50 + 1e-10) - 1,
            rsi_val / 100.0,
            float(sk), float(sd),
            1.0 if sk > sd else 0.0,
            float(mh),
            float(mh - mhp),
            float(mab),
            float(np.clip(bb_pos, -2, 2)),
            float(np.clip(vwap_pos, -0.05, 0.05)),
            float(np.clip(vol_ratio, 0, 5)),
            float(body_ratio),
            float(bull_candle),
            float(np.clip(ret1,  -0.1, 0.1)),
            float(np.clip(ret5,  -0.2, 0.2)),
            float(np.clip(ret10, -0.3, 0.3)),
            float(np.clip(atr_ratio, 0, 0.1)),
        ]
        # Replace any NaN/inf
        feats = [0.0 if (np.isnan(x) or np.isinf(x)) else x for x in feats]
        return feats
    except:
        return None


def build_ml_dataset(symbol, interval="1h", period="2y"):
    """
    Build labeled (X, y) dataset for ML training.
    Label 1 = price hit TP (ATR*1.4 up) before SL (ATR*1.2 down).
    Label 0 = price hit SL before TP.
    Ambiguous candles are skipped.
    """
    df = _get_fetch_data()(symbol, interval=interval, period=period)
    if df is None or len(df) < 120:
        return None, None

    X, y = [], []
    step = 2  # sample every 2nd candle for speed

    for i in range(60, len(df) - 20, step):
        slice_df = df.iloc[:i + 1]
        feats = extract_features(slice_df)
        if feats is None:
            continue

        entry = df['close'].iloc[i]
        atr   = get_atr(slice_df)
        if not atr or atr == 0:
            continue

        tp_up   = entry + atr * 1.4
        sl_down = entry - atr * 1.2
        tp_dn   = entry - atr * 1.4
        sl_up   = entry + atr * 1.2

        future = df.iloc[i + 1: i + 16]
        if len(future) < 5:
            continue

        # Determine if this was a bullish (1) or bearish (0) setup
        hit_tp_bull = (future['high'] >= tp_up).any()
        hit_sl_bull = (future['low']  <= sl_down).any()
        hit_tp_bear = (future['low']  <= tp_dn).any()
        hit_sl_bear = (future['high'] >= sl_up).any()

        # Only label clean wins/losses — skip ambiguous
        if hit_tp_bull and not hit_sl_bull:
            X.append(feats); y.append(1)
        elif hit_sl_bull and not hit_tp_bull:
            X.append(feats); y.append(0)
        elif hit_tp_bear and not hit_sl_bear:
            X.append(feats); y.append(0)
        elif hit_sl_bear and not hit_tp_bear:
            X.append(feats); y.append(1)

    if len(X) < 50:
        return None, None

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.int32)


def _training_thread(symbols, interval):
    """Runs in background thread. Trains model and saves to disk."""
    global _ML_MODEL, _ML_SCALER

    if not HAS_SKLEARN:
        with _ML_LOCK:
            _ML_STATE.update({"status": "error", "error": "scikit-learn not installed. Run: pip install scikit-learn xgboost"})
        return

    try:
        all_X, all_y = [], []
        n = len(symbols)

        for idx, sym in enumerate(symbols):
            with _ML_LOCK:
                pct = int((idx / n) * 60)
                _ML_STATE.update({"status": "training", "progress": pct,
                                  "message": f"Fetching {sym} ({idx+1}/{n})…"})
            X, y = build_ml_dataset(sym, interval=interval)
            if X is not None:
                all_X.append(X); all_y.append(y)

        if not all_X:
            with _ML_LOCK:
                _ML_STATE.update({"status": "error", "error": "No usable data returned from any symbol."})
            return

        with _ML_LOCK:
            _ML_STATE.update({"progress": 65, "message": "Combining datasets…"})

        X = np.vstack(all_X)
        y = np.hstack(all_y)
        n_samples = len(X)

        with _ML_LOCK:
            _ML_STATE.update({"progress": 70, "message": f"Training on {n_samples:,} samples…"})

        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_tr_s = scaler.fit_transform(X_tr)
        X_te_s = scaler.transform(X_te)

        if HAS_XGB:
            model = xgb.XGBClassifier(
                n_estimators=300, max_depth=5, learning_rate=0.05,
                subsample=0.8, colsample_bytree=0.8,
                random_state=42, eval_metric='logloss',
                use_label_encoder=False, verbosity=0,
            )
        else:
            model = GradientBoostingClassifier(
                n_estimators=200, max_depth=4, learning_rate=0.05,
                subsample=0.8, random_state=42,
            )

        with _ML_LOCK:
            _ML_STATE.update({"progress": 75, "message": "Fitting model…"})

        model.fit(X_tr_s, y_tr)

        with _ML_LOCK:
            _ML_STATE.update({"progress": 90, "message": "Evaluating…"})

        acc = round(accuracy_score(y_te, model.predict(X_te_s)) * 100, 1)

        # Feature importances
        imp = model.feature_importances_
        fi = sorted(zip(FEATURE_NAMES, imp.tolist()), key=lambda x: -x[1])

        # Save to disk
        with open(ML_MODEL_PATH,  'wb') as f: pickle.dump(model,  f)
        with open(ML_SCALER_PATH, 'wb') as f: pickle.dump(scaler, f)

        with _ML_LOCK:
            _ML_MODEL  = model
            _ML_SCALER = scaler
            _ML_STATE.update({
                "status": "done", "progress": 100,
                "message": f"Model trained — {acc}% test accuracy",
                "accuracy": acc, "n_samples": n_samples,
                "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "error": None, "feat_imp": fi,
            })

    except Exception as e:
        with _ML_LOCK:
            _ML_STATE.update({"status": "error", "error": str(e), "progress": 0})


def start_ml_training(symbols=None, interval="1h"):
    global _ML_MODEL, _ML_SCALER
    if symbols is None:
        symbols = ["BTC-USD", "ETH-USD", "SOL-USD", "NQ=F", "GC=F", "EURUSD=X"]
    with _ML_LOCK:
        if _ML_STATE["status"] == "training":
            return  # already running
        _ML_STATE.update({"status": "training", "progress": 0,
                          "message": "Starting…", "error": None})
    t = threading.Thread(target=_training_thread, args=(symbols, interval), daemon=True)
    t.start()


def load_ml_model():
    """Try to load saved model from disk on startup."""
    global _ML_MODEL, _ML_SCALER
    if not HAS_SKLEARN: return
    try:
        if os.path.exists(ML_MODEL_PATH) and os.path.exists(ML_SCALER_PATH):
            with open(ML_MODEL_PATH,  'rb') as f: model  = pickle.load(f)
            with open(ML_SCALER_PATH, 'rb') as f: scaler = pickle.load(f)
            imp = model.feature_importances_
            fi = sorted(zip(FEATURE_NAMES, imp.tolist()), key=lambda x: -x[1])
            with _ML_LOCK:
                _ML_MODEL  = model
                _ML_SCALER = scaler
                _ML_STATE.update({
                    "status": "done",
                    "message": "Model loaded from disk.",
                    "accuracy": None,
                    "trained_at": "Loaded from file",
                    "feat_imp": fi,
                })
    except:
        pass


def ml_predict(df):
    """Return (bull_prob %, bear_prob %). Both None if model not ready."""
    with _ML_LOCK:
        model  = _ML_MODEL
        scaler = _ML_SCALER
    if model is None or scaler is None:
        return None, None
    feats = extract_features(df)
    if feats is None:
        return None, None
    try:
        X = np.array(feats, dtype=np.float32).reshape(1, -1)
        X_s = scaler.transform(X)
        proba = model.predict_proba(X_s)[0]
        return round(proba[1] * 100, 1), round(proba[0] * 100, 1)
    except:
        return None, None


# ── BACKTESTING ENGINE ────────────────────────────────────────────────────────

def _backtest_thread(symbol, interval, period="2y"):
    with _BT_LOCK:
        _BT_STATE.update({"status": "running", "progress": 5,
                          "message": f"Fetching {symbol} {interval} data…", "results": None})
    try:
        df = _get_fetch_data()(symbol, interval=interval, period=period)
        if df is None or len(df) < 120:
            with _BT_LOCK:
                _BT_STATE.update({"status": "error",
                                  "message": f"Not enough data for {symbol} {interval}"})
            return

        trades = []
        factor_stats = {}   # factor_name -> {"wins":0, "total":0}
        monthly_wr = {}

        n = len(df)
        step = 3  # check every 3rd candle

        for i in range(60, n - 20, step):
            pct = int(5 + (i / n) * 85)
            if i % 90 == 0:
                with _BT_LOCK:
                    _BT_STATE.update({"progress": pct,
                                      "message": f"Testing candle {i}/{n}…"})

            slice_df = df.iloc[:i + 1]
            if len(slice_df) < 60:
                continue

            # Lightweight signal (no HTF fetch in backtest)
            cl = slice_df['close']
            last = cl.iloc[-1]
            bull = bear = 0
            fired = {}

            ema_t = get_ema_trend(slice_df)
            if ema_t == "bullish":   bull += 18; fired["EMA Trend"] = "bull"
            elif ema_t == "bearish": bear += 18; fired["EMA Trend"] = "bear"

            try:
                rsi_v = ta.momentum.RSIIndicator(cl, 14).rsi().iloc[-1]
                if rsi_v < 45:   bull += 10; fired["RSI"] = "bull"
                elif rsi_v > 55: bear += 10; fired["RSI"] = "bear"
            except: pass

            try:
                m_ = ta.trend.MACD(cl)
                if m_.macd().iloc[-1] > m_.macd_signal().iloc[-1]: bull += 8; fired["MACD"] = "bull"
                else: bear += 8; fired["MACD"] = "bear"
            except: pass

            vwap_s = get_vwap_series(slice_df)
            if vwap_s is not None:
                if last > vwap_s.iloc[-1]: bull += 8; fired["VWAP"] = "bull"
                else: bear += 8; fired["VWAP"] = "bear"

            if len(slice_df) >= 20:
                bm = cl.rolling(20).mean().iloc[-1]
                bs = cl.rolling(20).std().iloc[-1]
                if last <= bm - 2*bs: bull += 6; fired["Bollinger"] = "bull"
                elif last >= bm + 2*bs: bear += 6; fired["Bollinger"] = "bear"

            div = get_rsi_divergence(slice_df)
            if div == "bullish":   bull += 12; fired["RSI Divergence"] = "bull"
            elif div == "bearish": bear += 12; fired["RSI Divergence"] = "bear"

            conf = max(bull, bear)
            if conf < 55 or abs(bull - bear) < 12:
                continue  # no signal

            signal = "BUY" if bull > bear else "SELL"

            entry = last
            atr = get_atr(slice_df)
            if not atr: continue
            tp = entry + atr * 1.4 if signal == "BUY" else entry - atr * 1.4
            sl = entry - atr * 1.2 if signal == "BUY" else entry + atr * 1.2

            # Look ahead up to 20 candles
            result = "timeout"
            for j in range(i + 1, min(i + 21, n)):
                h = df['high'].iloc[j]; lo = df['low'].iloc[j]
                if signal == "BUY":
                    if h >= tp:  result = "win";  break
                    if lo <= sl: result = "loss"; break
                else:
                    if lo <= tp: result = "win";  break
                    if h >= sl:  result = "loss"; break

            if result == "timeout":
                continue

            # Monthly tracking
            month_key = df.index[i].strftime("%Y-%m")
            if month_key not in monthly_wr:
                monthly_wr[month_key] = {"wins": 0, "losses": 0}
            if result == "win":   monthly_wr[month_key]["wins"]   += 1
            else:                 monthly_wr[month_key]["losses"] += 1

            # Factor tracking
            for fname, fdir in fired.items():
                matches_signal = (fdir == "bull" and signal == "BUY") or (fdir == "bear" and signal == "SELL")
                if matches_signal:
                    if fname not in factor_stats:
                        factor_stats[fname] = {"wins": 0, "total": 0}
                    factor_stats[fname]["total"] += 1
                    if result == "win":
                        factor_stats[fname]["wins"] += 1

            trades.append({"signal": signal, "confidence": conf, "result": result,
                           "entry": round(entry, 6), "month": month_key})

        # Summarise
        wins   = sum(1 for t in trades if t["result"] == "win")
        losses = sum(1 for t in trades if t["result"] == "loss")
        total  = wins + losses
        win_rate = round(wins / total * 100, 1) if total > 0 else 0

        # Factor accuracy sorted
        factor_acc = []
        for fname, stats in factor_stats.items():
            wr = round(stats["wins"] / stats["total"] * 100, 1) if stats["total"] > 0 else 0
            factor_acc.append({"name": fname, "wr": wr, "total": stats["total"]})
        factor_acc.sort(key=lambda x: -x["wr"])

        # High-confidence WR
        hc_trades = [t for t in trades if t["confidence"] >= 80]
        hc_wins   = sum(1 for t in hc_trades if t["result"] == "win")
        hc_wr     = round(hc_wins / len(hc_trades) * 100, 1) if hc_trades else 0

        # Best / worst months
        best_month  = max(monthly_wr.items(), key=lambda x: x[1]["wins"] / max(x[1]["wins"]+x[1]["losses"],1), default=(None,{}))
        worst_month = min(monthly_wr.items(), key=lambda x: x[1]["wins"] / max(x[1]["wins"]+x[1]["losses"],1), default=(None,{}))

        results = {
            "symbol": symbol, "interval": interval,
            "total": total, "wins": wins, "losses": losses,
            "win_rate": win_rate,
            "hc_wr": hc_wr, "hc_trades": len(hc_trades),
            "factor_acc": factor_acc,
            "monthly_wr": monthly_wr,
            "best_month": best_month[0],
            "worst_month": worst_month[0],
            "recent_trades": trades[-30:],
        }

        with _BT_LOCK:
            _BT_STATE.update({"status": "done", "progress": 100,
                              "message": f"Done — {win_rate}% win rate on {total} trades",
                              "results": results})
    except Exception as e:
        with _BT_LOCK:
            _BT_STATE.update({"status": "error", "message": str(e), "results": None})


def start_backtest(symbol, interval):
    with _BT_LOCK:
        if _BT_STATE["status"] == "running":
            return
        _BT_STATE.update({"status": "running", "progress": 0,
                          "message": "Starting backtest…", "results": None})
    t = threading.Thread(target=_backtest_thread, args=(symbol, interval), daemon=True)
    t.start()


# ── AI LAB RENDER HELPERS ─────────────────────────────────────────────────────

def _prog_bar(pct, color=PURPLE):
    return html.Div(
        html.Div(className="prog-bar-fill",
                 style={"width": f"{pct}%", "backgroundColor": color, "height": "100%", "borderRadius": "4px"}),
        style={"backgroundColor": "#1e1a2e", "borderRadius": "4px", "height": "6px",
               "marginTop": "4px", "marginBottom": "4px"})


def render_feat_importance(fi):
    if not fi:
        return html.Div("Train the model to see feature importance.",
                        style={"color": TEXT_MUTED, "fontSize": "0.72em", "fontStyle": "italic"})
    top = fi[:10]
    max_imp = top[0][1] if top else 1
    rows = []
    for name, imp in top:
        pct = int(imp / max_imp * 100) if max_imp else 0
        rows.append(html.Div([
            html.Div(name, style={"color": TEXT_DIM, "fontSize": "0.65em", "width": "95px",
                                  "flexShrink": "0", "textOverflow": "ellipsis", "overflow": "hidden",
                                  "whiteSpace": "nowrap"}),
            html.Div(html.Div(style={"width": f"{pct}%", "backgroundColor": PURPLE,
                                     "height": "100%", "borderRadius": "2px"}),
                     style={"flex": "1", "backgroundColor": "#1e1a2e", "height": "6px",
                            "borderRadius": "2px", "margin": "0 8px", "alignSelf": "center"}),
            html.Div(f"{imp:.3f}", style={"color": TEXT_MUTED, "fontSize": "0.62em", "width": "36px",
                                           "textAlign": "right", "flexShrink": "0"}),
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "5px"}))
    return html.Div(rows)


def render_backtest_results(res):
    if not res:
        return html.Div("No results yet.", style={"color": TEXT_MUTED, "fontSize": "0.72em"})

    wr_color = BULL if res["win_rate"] >= 55 else BEAR if res["win_rate"] < 45 else NEUTRAL

    items = [
        # headline stats
        html.Div([
            _stat_mini("Win Rate", f"{res['win_rate']}%", wr_color),
            _stat_mini("Trades",   str(res["total"]),   TEXT_MAIN),
            _stat_mini("Wins",     str(res["wins"]),    BULL),
            _stat_mini("Losses",   str(res["losses"]),  BEAR),
        ], style={"display": "flex", "gap": "6px", "marginBottom": "12px", "flexWrap": "wrap"}),
        html.Div([
            _stat_mini("High-Conf WR", f"{res['hc_wr']}%",
                       BULL if res['hc_wr'] >= 60 else NEUTRAL),
            _stat_mini("HC Trades", str(res["hc_trades"]), TEXT_DIM),
        ], style={"display": "flex", "gap": "6px", "marginBottom": "14px"}),
        # Win rate bar
        html.Div([
            html.Div("OVERALL WIN RATE", style={"color": TEXT_MUTED, "fontSize": "0.58em",
                                                 "letterSpacing": "1px", "marginBottom": "3px"}),
            _prog_bar(int(res["win_rate"]), wr_color),
        ], style={"marginBottom": "14px"}),
        # Factor accuracy
        html.Div("FACTOR ACCURACY", style={"color": TEXT_MUTED, "fontSize": "0.58em",
                                            "letterSpacing": "1px", "marginBottom": "6px",
                                            "fontWeight": "600"}),
    ]

    for fa in res.get("factor_acc", [])[:7]:
        fc = BULL if fa["wr"] >= 60 else BEAR if fa["wr"] < 50 else NEUTRAL
        items.append(html.Div([
            html.Div(fa["name"], style={"color": TEXT_DIM, "fontSize": "0.66em", "width": "110px", "flexShrink": "0"}),
            html.Div(html.Div(style={"width": f"{int(fa['wr'])}%", "backgroundColor": fc,
                                      "height": "100%", "borderRadius": "2px"}),
                     style={"flex": "1", "backgroundColor": "#1e1a2e", "height": "5px",
                            "borderRadius": "2px", "margin": "0 6px", "alignSelf": "center"}),
            html.Div(f"{fa['wr']}%", style={"color": fc, "fontSize": "0.64em",
                                              "fontWeight": "600", "width": "34px", "textAlign": "right"}),
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "5px"}))

    if res.get("best_month"):
        bm = res["best_month"]
        bm_d = res["monthly_wr"].get(bm, {})
        bm_tot = bm_d.get("wins", 0) + bm_d.get("losses", 0)
        bm_wr = round(bm_d.get("wins", 0) / bm_tot * 100) if bm_tot else 0
        items.append(html.Div(
            f"📈  Best month: {bm}  ({bm_wr}% WR, {bm_tot} trades)",
            style={"color": BULL, "fontSize": "0.65em", "marginTop": "10px",
                   "backgroundColor": "rgba(52,211,153,0.06)",
                   "border": "1px solid rgba(52,211,153,0.2)",
                   "borderRadius": "6px", "padding": "6px 10px"}))

    if res.get("worst_month"):
        wm = res["worst_month"]
        wm_d = res["monthly_wr"].get(wm, {})
        wm_tot = wm_d.get("wins", 0) + wm_d.get("losses", 0)
        wm_wr = round(wm_d.get("wins", 0) / wm_tot * 100) if wm_tot else 0
        items.append(html.Div(
            f"📉  Worst month: {wm}  ({wm_wr}% WR, {wm_tot} trades)",
            style={"color": BEAR, "fontSize": "0.65em", "marginTop": "5px",
                   "backgroundColor": "rgba(248,113,113,0.06)",
                   "border": "1px solid rgba(248,113,113,0.2)",
                   "borderRadius": "6px", "padding": "6px 10px"}))

    return html.Div(items)


def _stat_mini(label, value, color):
    return html.Div([
        html.Div(value, style={"color": color, "fontWeight": "700", "fontSize": "1.1em",
                                "lineHeight": "1.1"}),
        html.Div(label, style={"color": TEXT_MUTED, "fontSize": "0.58em", "marginTop": "2px"}),
    ], style={"backgroundColor": BG_CARD, "border": f"1px solid {BORDER}", "borderRadius": "7px",
               "padding": "8px 11px", "flex": "1", "minWidth": "60px", "textAlign": "center"})


# Try loading saved model on startup -- auto-train if none found
load_ml_model()
# Try loading saved model on startup -- auto-train if none found
load_ml_model()
with _ML_LOCK:
    _model_missing = (_ML_MODEL is None)
if _model_missing and HAS_SKLEARN:
    start_ml_training(
        symbols=["BTC-USD","ETH-USD","SOL-USD","NQ=F","GC=F","EURUSD=X"],
        interval="1h"
    )
