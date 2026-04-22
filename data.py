# ══════════════════════════════════════════════════════════════════════════════
#  data.py  —  Data fetching, signal engine, pattern detection, news
# ══════════════════════════════════════════════════════════════════════════════

import yfinance as yf
import requests as http_req
import xml.etree.ElementTree as ET
import time
import pandas as pd
import numpy as np
import ta
from dash import html
from datetime import datetime, timezone

from config import (
    PLAN_LIMITS, HIGHER_TF, HIGHER_PERIOD, ALL_PATTERNS, DESCS, PAT_COLOR,
    NEWS_SOURCES, NEWS_CAT_COLORS, NEWS_CAT_ICONS, NEUTRAL, TEXT_MAIN, TEXT_MUTED,
    BORDER, BULL, BEAR,
)
# ml_predict is imported lazily inside superintelligent_signal() to avoid circular imports


def fetch_data(symbol,interval="5m",period="5d"):
    try:
        # yfinance does not support 2h or 3h — resample from 1h
        if interval in ("2h","3h"):
            df=yf.Ticker(symbol).history(period=period,interval="1h")
            if df.empty: return None
            df.index=pd.to_datetime(df.index); df.columns=[c.lower() for c in df.columns]
            rule="2h" if interval=="2h" else "3h"
            ohlc_d={"open":"first","high":"max","low":"min","close":"last","volume":"sum"}
            cols=[c for c in ["open","high","low","close","volume"] if c in df.columns]
            df=df[cols].resample(rule,closed="left",label="left").agg({c:ohlc_d[c] for c in cols}).dropna()
            return df if not df.empty else None
        df=yf.Ticker(symbol).history(period=period,interval=interval)
        if df.empty: return None
        df.index=pd.to_datetime(df.index); df.columns=[c.lower() for c in df.columns]
        return df
    except: return None

def get_atr(df,period=14):
    if df is None or len(df)<period: return None
    return round((df['high']-df['low']).rolling(period).mean().iloc[-1],6)

def get_htf_bias(symbol,interval):
    try:
        htf=HIGHER_TF.get(interval,"1h"); per=HIGHER_PERIOD.get(htf,"1mo")
        df=fetch_data(symbol,interval=htf,period=per)
        if df is None or len(df)<50: return "neutral"
        cl=df['close']; e20=cl.ewm(span=20,adjust=False).mean().iloc[-1]; e50=cl.ewm(span=50,adjust=False).mean().iloc[-1]; last=cl.iloc[-1]
        if last>e20>e50: return "bullish"
        if last<e20<e50: return "bearish"
        return "neutral"
    except: return "neutral"

def get_vwap_series(df):
    if df is None or 'volume' not in df.columns or len(df)<2: return None
    try:
        tp=(df['high']+df['low']+df['close'])/3; vol=df['volume'].replace(0,np.nan).fillna(1)
        return (tp*vol).cumsum()/vol.cumsum()
    except: return None

def get_rsi_divergence(df,lookback=20):
    if df is None or len(df)<lookback+5: return None
    try:
        cl=df['close'].values[-lookback:]; rsi=ta.momentum.RSIIndicator(df['close'],14).rsi().values[-lookback:]
        lows=[i for i in range(1,len(cl)-1) if cl[i]<cl[i-1] and cl[i]<cl[i+1]]
        highs=[i for i in range(1,len(cl)-1) if cl[i]>cl[i-1] and cl[i]>cl[i+1]]
        if len(lows)>=2:
            p1,p2=lows[-2],lows[-1]
            if cl[p2]<cl[p1] and rsi[p2]>rsi[p1]: return "bullish"
        if len(highs)>=2:
            p1,p2=highs[-2],highs[-1]
            if cl[p2]>cl[p1] and rsi[p2]<rsi[p1]: return "bearish"
        return None
    except: return None

def get_volatility_state(df,period=14):
    if df is None or len(df)<period*2: return "good"
    try:
        s=(df['high']-df['low']).rolling(period).mean(); c=s.iloc[-1]; a=s.iloc[-period*2:-period].mean()
        if a==0: return "good"
        r=c/a
        if r<0.4: return "too_low"
        if r>3.0: return "too_high"
        return "good"
    except: return "good"

def is_good_session(symbol):
    crypto=["BTC-USD","ETH-USD","BNB-USD","SOL-USD","XRP-USD","DOGE-USD","ADA-USD","AVAX-USD","DOT-USD","MATIC-USD","LINK-USD","UNI-USD","ATOM-USD","LTC-USD","BCH-USD","NEAR-USD","APT-USD","OP-USD","ARB-USD","TON-USD","SUI-USD","TRX-USD","SHIB-USD","PEPE-USD"]
    if symbol in crypto: return True
    now=datetime.now(timezone.utc); h=now.hour+now.minute/60; wd=now.weekday()
    if wd>=5: return False
    if h<7.5 or h>20.0: return False
    return True

def get_sr_confluence(df,signal,tolerance=0.003):
    if df is None or len(df)<30: return 0
    try:
        last=df['close'].iloc[-1]; window=10; highs=df['high'].values; lows=df['low'].values
        sup_raw=[]; res_raw=[]
        for i in range(window,len(df)-window):
            if highs[i]==max(highs[i-window:i+window]): res_raw.append(highs[i])
            if lows[i]==min(lows[i-window:i+window]):   sup_raw.append(lows[i])
        def near(levels,price): return any(abs(lv-price)/max(price,0.0001)<tolerance for lv in levels)
        if signal=="BUY" and near(sup_raw,last): return 10
        if signal=="SELL" and near(res_raw,last): return 10
        return 0
    except: return 0

def is_spike_candle(df,multiplier=2.8):
    if df is None or len(df)<20: return False
    try:
        bodies=abs(df['close']-df['open'])
        return bodies.iloc[-1]>bodies.iloc[-20:-1].mean()*multiplier
    except: return False

def get_ema_trend(df):
    if df is None or len(df)<50: return "neutral"
    cl=df['close']
    e10=cl.ewm(span=10,adjust=False).mean().iloc[-1]; e20=cl.ewm(span=20,adjust=False).mean().iloc[-1]; e50=cl.ewm(span=50,adjust=False).mean().iloc[-1]; last=cl.iloc[-1]
    if e10>e20>e50 and last>e50: return "bullish"
    if e10<e20<e50 and last<e50: return "bearish"
    return "neutral"

def get_stoch_rsi(df):
    if df is None or len(df)<30: return None,None
    try:
        s=ta.momentum.StochRSIIndicator(df['close'],14,14,3,3)
        return round(s.stochrsi_k().iloc[-1],3),round(s.stochrsi_d().iloc[-1],3)
    except: return None,None

def superintelligent_signal(df,symbol,interval,patterns,plan="admin"):
    if df is None or len(df)<50: return "WAIT",NEUTRAL,0,{},"neutral"
    limits=PLAN_LIMITS.get(plan,PLAN_LIMITS[None])
    bull=0; bear=0; reasons={}; cl=df['close']; last=cl.iloc[-1]
    vol_state=get_volatility_state(df)
    if vol_state=="too_low": return "WAIT",NEUTRAL,0,{"Volatility":"⚠️ Market too quiet — no edge"},"neutral"
    if vol_state=="too_high": return "WAIT",NEUTRAL,0,{"Volatility":"⚠️ Extreme volatility — too risky"},"neutral"
    if not is_good_session(symbol): return "WAIT",NEUTRAL,0,{"Session":"💤 Low liquidity session — skipping"},"neutral"
    if is_spike_candle(df): return "WAIT",NEUTRAL,0,{"Spike":"⚡ Spike candle — likely reversal"},"neutral"
    ema_trend=get_ema_trend(df)
    if ema_trend=="bullish":   bull+=18; reasons["EMA Trend"]="✅ EMA stack bullish"
    elif ema_trend=="bearish": bear+=18; reasons["EMA Trend"]="✅ EMA stack bearish"
    else: reasons["EMA Trend"]="↔️ EMA mixed"
    if limits["htf"]:
        htf_bias=get_htf_bias(symbol,interval)
        if htf_bias=="bullish":   bull+=20; reasons["Higher TF"]="✅ Higher TF bullish"
        elif htf_bias=="bearish": bear+=20; reasons["Higher TF"]="✅ Higher TF bearish"
        else: reasons["Higher TF"]="↔️ Higher TF neutral"
    else:
        htf_bias="neutral"; reasons["Higher TF"]="🔒 Upgrade for HTF analysis"
    rsi_val=ta.momentum.RSIIndicator(cl,14).rsi().iloc[-1]
    if rsi_val<45:   bull+=10; reasons["RSI"]=f"✅ RSI {round(rsi_val,1)} oversold"
    elif rsi_val>55: bear+=10; reasons["RSI"]=f"✅ RSI {round(rsi_val,1)} overbought"
    else: reasons["RSI"]=f"↔️ RSI {round(rsi_val,1)} neutral"
    sk,sd=get_stoch_rsi(df)
    if sk is not None and sd is not None:
        if sk<0.2 and sk>sd:   bull+=8; reasons["StochRSI"]="✅ Oversold + K crossing up"
        elif sk>0.8 and sk<sd: bear+=8; reasons["StochRSI"]="✅ Overbought + K crossing down"
        else: reasons["StochRSI"]=f"↔️ Neutral ({round(sk,2)})"
    m=ta.trend.MACD(cl); mv=m.macd().iloc[-1]; ms=m.macd_signal().iloc[-1]; mh=m.macd_diff().iloc[-1]; prev_mh=m.macd_diff().iloc[-2] if len(df)>2 else 0
    if mv>ms and mh>0 and mh>prev_mh:   bull+=10; reasons["MACD"]="✅ Bullish + histogram rising"
    elif mv<ms and mh<0 and mh<prev_mh: bear+=10; reasons["MACD"]="✅ Bearish + histogram falling"
    elif mv>ms: bull+=5; reasons["MACD"]="✅ Bullish cross"
    elif mv<ms: bear+=5; reasons["MACD"]="✅ Bearish cross"
    else: reasons["MACD"]="↔️ Flat"
    vwap_s=get_vwap_series(df)
    if vwap_s is not None:
        vwap_last=vwap_s.iloc[-1]
        if last>vwap_last*1.001:   bull+=8; reasons["VWAP"]="✅ Price above VWAP"
        elif last<vwap_last*0.999: bear+=8; reasons["VWAP"]="✅ Price below VWAP"
        else: reasons["VWAP"]="↔️ Price at VWAP"
    if limits["divergence"]:
        div=get_rsi_divergence(df)
        if div=="bullish":   bull+=12; reasons["RSI Divergence"]="🔥 Bullish divergence"
        elif div=="bearish": bear+=12; reasons["RSI Divergence"]="🔥 Bearish divergence"
        else: reasons["RSI Divergence"]="↔️ No divergence"
    else: reasons["RSI Divergence"]="🔒 Upgrade for divergence"
    pb=min(sum(1 for _,s,_ in patterns if s=="bullish")*3,12); bb_=min(sum(1 for _,s,_ in patterns if s=="bearish")*3,12)
    bull+=pb; bear+=bb_
    pat_b=sum(1 for _,s,_ in patterns if s=="bullish"); pat_bear=sum(1 for _,s,_ in patterns if s=="bearish")
    if pat_b>0: reasons["Patterns"]=f"✅ {pat_b} bullish pattern(s)"
    elif pat_bear>0: reasons["Patterns"]=f"✅ {pat_bear} bearish pattern(s)"
    else: reasons["Patterns"]="↔️ No strong patterns"
    direction="BUY" if bull>bear else "SELL"; cb=get_sr_confluence(df,direction)
    if cb>0:
        if direction=="BUY":  bull+=cb; reasons["S/R Level"]="🔥 Entry at key support"
        else:                 bear+=cb; reasons["S/R Level"]="🔥 Entry at key resistance"
    else: reasons["S/R Level"]="↔️ No S/R confluence"
    if len(df)>=20:
        bm=cl.rolling(20).mean().iloc[-1]; bs=cl.rolling(20).std().iloc[-1]; bu=bm+2*bs; bl=bm-2*bs
        if last<=bl*1.002:   bull+=6; reasons["Bollinger"]="✅ At lower band"
        elif last>=bu*0.998: bear+=6; reasons["Bollinger"]="✅ At upper band"
        elif last>bm: bull+=2; reasons["Bollinger"]="↔️ Above midline"
        else: bear+=2; reasons["Bollinger"]="↔️ Below midline"
    if 'volume' in df.columns and len(df)>=10:
        avg_v=df['volume'].iloc[-10:-1].mean(); cur_v=df['volume'].iloc[-1]; vol_ok=cur_v>avg_v*1.2; cur_bull=df['close'].iloc[-1]>df['open'].iloc[-1]
        if vol_ok and cur_bull:       bull+=6; reasons["Volume"]="✅ High volume bull candle"
        elif vol_ok and not cur_bull: bear+=6; reasons["Volume"]="✅ High volume bear candle"
        else: reasons["Volume"]="↔️ Average volume"
    htf_ok=htf_bias in ["bullish","neutral"] if bull>bear else htf_bias in ["bearish","neutral"]

    # ── ML boost: if model trained, adjust confidence ──────────────────────
    ml_note = ""
    try:
        import ml as _ml_module
        with _ml_module._ML_LOCK:
            model_ready = (_ml_module._ML_MODEL is not None and _ml_module._ML_SCALER is not None)
    except Exception:
        model_ready = False
    if model_ready:
        from ml import ml_predict
        bull_prob, bear_prob = ml_predict(df)
        if bull_prob is not None:
            if bull > bear:   # manual says BUY
                boost = int((bull_prob - 50) * 0.18) if bull_prob > 50 else int((bull_prob - 50) * 0.12)
                bull = max(0, bull + boost)
                ml_note = f"🧠 ML: Bull {bull_prob}%"
            else:             # manual says SELL
                boost = int((bear_prob - 50) * 0.18) if bear_prob > 50 else int((bear_prob - 50) * 0.12)
                bear = max(0, bear + boost)
                ml_note = f"🧠 ML: Bear {bear_prob}%"
            reasons["ML Model"] = ml_note if ml_note else "↔️ ML: neutral"

    if bull>=62 and bull-bear>=15 and htf_ok: return "BUY",BULL,min(int((bull/100)*100),99),reasons,ema_trend
    elif bear>=62 and bear-bull>=15 and htf_ok: return "SELL",BEAR,min(int((bear/100)*100),99),reasons,ema_trend
    else: return "WAIT",NEUTRAL,min(int((max(bull,bear)/100)*100),55),reasons,ema_trend

def get_levels(df, signal, custom_tp=None, custom_sl=None):
    """
    Advanced TP/SL engine — uses market structure, not fixed ATR multiples.

    Stop Loss logic (priority order):
      1. Place just below/above the most recent significant swing low/high
         (last 15 candles, buffered by 0.25× ATR so wicks don't trigger it)
      2. If no clean swing found, fall back to 1.8× ATR from entry

    Take Profit logic (priority order):
      1. Nearest hard S/R level on the correct side with ≥ 1.5:1 R:R
      2. Fibonacci 0.618 extension of the most recent swing range
      3. Minimum guaranteed 1.8:1 R:R target as fallback

    Final check: if computed R:R < 1.5 the TP is pushed out to enforce 1.5:1.
    """
    if df is None or len(df) < 20 or signal == "WAIT":
        return None, None, None

    last = df['close'].iloc[-1]
    atr  = get_atr(df)
    if atr is None or atr == 0:
        return None, None, None

    # ── STOP LOSS ────────────────────────────────────────────────────────────
    lookback = min(20, len(df) - 1)
    recent   = df.iloc[-lookback:]

    if signal == "BUY":
        # Swing low = lowest LOW in the lookback window
        swing_extreme = recent['low'].min()
        sl_struct     = swing_extreme - atr * 0.25          # buffer below the wick
        sl_atr        = last - atr * 1.8                    # ATR fallback
        # Use whichever is CLOSER to the current price (tighter, less risk)
        sl = max(sl_struct, sl_atr)
        # Hard cap: never more than 3.5× ATR away (avoid runaway SL)
        sl = max(sl, last - atr * 3.5)
    else:  # SELL
        swing_extreme = recent['high'].max()
        sl_struct     = swing_extreme + atr * 0.25
        sl_atr        = last + atr * 1.8
        sl = min(sl_struct, sl_atr)
        sl = min(sl, last + atr * 3.5)

    risk = abs(last - sl)
    if risk == 0:
        risk = atr * 1.5

    # ── TAKE PROFIT ──────────────────────────────────────────────────────────
    sup_levels, res_levels = get_support_resistance(df)

    # Minimum TP to guarantee 1.5:1 R:R
    min_tp = last + risk * 1.5 if signal == "BUY" else last - risk * 1.5

    # Fibonacci 0.618 extension of the recent swing range
    swing_range = recent['high'].max() - recent['low'].min()
    fib_tp = last + swing_range * 0.618 if signal == "BUY" else last - swing_range * 0.618

    # Nearest S/R level that clears the minimum R:R requirement
    sr_tp = None
    if signal == "BUY" and res_levels:
        candidates = [r for r in res_levels if r >= min_tp]
        sr_tp = min(candidates) if candidates else None
    elif signal == "SELL" and sup_levels:
        candidates = [s for s in sup_levels if s <= min_tp]
        sr_tp = max(candidates) if candidates else None

    # Pick the best (most conservative = nearest realistic target)
    tp_options = []
    if sr_tp is not None:
        tp_options.append(sr_tp)
    if signal == "BUY" and fib_tp >= min_tp:
        tp_options.append(fib_tp)
    elif signal == "SELL" and fib_tp <= min_tp:
        tp_options.append(fib_tp)

    if tp_options:
        tp = min(tp_options) if signal == "BUY" else max(tp_options)
    else:
        # Pure R:R fallback — 1.8:1
        tp = last + risk * 1.8 if signal == "BUY" else last - risk * 1.8

    # Final sanity: enforce minimum 1.5:1 R:R
    if signal == "BUY" and tp < min_tp:
        tp = min_tp
    elif signal == "SELL" and tp > min_tp:
        tp = min_tp

    entry = round(last, 6)
    tp    = round(float(custom_tp) if custom_tp else tp, 6)
    sl    = round(float(custom_sl) if custom_sl else sl, 6)
    return entry, tp, sl

def get_indicators(df):
    if df is None or len(df)<26: return None,None,None,None
    cl=df['close']; rsi=ta.momentum.RSIIndicator(cl,14).rsi().iloc[-1]; m=ta.trend.MACD(cl)
    return round(rsi,2),round(m.macd().iloc[-1],6),round(m.macd_signal().iloc[-1],6),cl.iloc[-1]

def get_bollinger_bands(df,period=20,std_dev=2):
    if df is None or len(df)<period: return None,None,None
    cl=df['close']; ma=cl.rolling(period).mean(); std=cl.rolling(period).std()
    return ma,ma+std_dev*std,ma-std_dev*std

def get_support_resistance(df,window=10,max_levels=3):
    if df is None or len(df)<window*3: return [],[]
    highs=df['high'].values; lows=df['low'].values; res_raw=[]; sup_raw=[]
    for i in range(window,len(df)-window):
        if highs[i]==max(highs[i-window:i+window]): res_raw.append(highs[i])
        if lows[i]==min(lows[i-window:i+window]):   sup_raw.append(lows[i])
    def cluster(levels,tol=0.002):
        if not levels: return []
        levels=sorted(set(levels)); out=[]; grp=[levels[0]]
        for lv in levels[1:]:
            if (lv-grp[-1])/max(grp[-1],0.0001)<tol: grp.append(lv)
            else: out.append(sum(grp)/len(grp)); grp=[lv]
        out.append(sum(grp)/len(grp)); return out
    last=df['close'].iloc[-1]; res=cluster(res_raw); sup=cluster(sup_raw)
    return sorted([s for s in sup if s<last],reverse=True)[:max_levels],sorted([r for r in res if r>last])[:max_levels]

def get_prev_day_levels(df):
    if df is None or len(df)<2: return None,None
    try:
        today=df.index[-1].date(); prev=df[pd.to_datetime(df.index).date<today]
        if len(prev)==0: return None,None
        yday=pd.to_datetime(prev.index).date[-1]; yd=prev[pd.to_datetime(prev.index).date==yday]
        if len(yd)==0: return None,None
        return round(yd['high'].max(),6),round(yd['low'].min(),6)
    except: return None,None

def get_summary(signal,ema_trend,rsi,in_cooldown=False,reasons=None):
    if in_cooldown: return "Bojket is analyzing the market after your last trade. Waiting for the next high-confidence setup."
    if signal=="BUY" and ema_trend=="bullish": return "Multi-timeframe aligned bullish. EMA stack, momentum and volume confirm. High-quality setup."
    if signal=="SELL" and ema_trend=="bearish": return "Multi-timeframe aligned bearish. EMA stack, momentum and volume confirm. High-quality setup."
    if signal=="WAIT":
        if reasons:
            for k in ["Volatility","Session","Spike"]:
                if k in reasons: return reasons[k]
        return "No edge detected. All conditions must align before Bojket signals. Stay patient."
    return "Conditions partially aligned. Waiting for full confirmation across all timeframes."

def get_streak(journal):
    if not journal: return 0
    streak=0
    for t in reversed(journal):
        if "TP" in str(t.get("result","")): streak+=1
        else: break
    return streak

def calc_pnl(signal,entry,current,position_size):
    try:
        e=float(entry); c=float(current); ps=float(position_size)
        return round((c-e)*ps if signal=="BUY" else (e-c)*ps,4)
    except: return None

def detect_single(name,op,hi,lo,cl,pop,phi,plo,pcl,p2op,p2cl,body,fr,uw,lw,pb):
    if name=="Doji": return body/fr<0.1
    if name=="Hammer": return lw>2*body and uw<body and cl>op
    if name=="Inverted Hammer": return uw>2*body and lw<body and cl>op
    if name=="Hanging Man": return lw>2*body and uw<body and cl<op
    if name=="Shooting Star": return uw>2*body and lw<body and cl<op
    if name=="Bullish Marubozu": return cl>op and uw<body*0.05 and lw<body*0.05
    if name=="Bearish Marubozu": return cl<op and uw<body*0.05 and lw<body*0.05
    if name=="Spinning Top": return body/fr<0.3 and uw>body and lw>body
    if name=="High Wave": return uw>3*body and lw>3*body
    if name=="Bullish Engulfing": return cl>op and pcl<pop and cl>pop and op<pcl
    if name=="Bearish Engulfing": return cl<op and pcl>pop and cl<pop and op>pcl
    if name=="Bullish Harami": return pop>pcl and cl>op and op>pcl and cl<pop
    if name=="Bearish Harami": return pcl>pop and cl<op and op<pcl and cl>pop
    if name=="Tweezer Tops": return abs(hi-phi)/fr<0.02 and cl<op and pcl>pop
    if name=="Tweezer Bottoms": return abs(lo-plo)/fr<0.02 and cl>op and pcl<pop
    if name=="Dark Cloud Cover": return pcl>pop and cl<op and op>phi and cl<(pop+(pcl-pop)/2)
    if name=="Piercing Line": return pcl<pop and cl>op and op<plo and cl>(pop+(pcl-pop)/2)
    if name=="Morning Star": return p2cl<p2op and abs(pcl-pop)<pb*0.3 and cl>op and cl>(p2op+p2cl)/2
    if name=="Evening Star": return p2cl>p2op and abs(pcl-pop)<pb*0.3 and cl<op and cl<(p2op+p2cl)/2
    if name=="Three White Soldiers": return cl>op and pcl>pop and p2cl>p2op and cl>pcl and pcl>p2cl
    if name=="Three Black Crows": return cl<op and pcl<pop and p2cl<p2op and cl<pcl and pcl<p2cl
    if name=="Three Inside Up": return p2cl<p2op and pcl>pop and pop>p2cl and pcl<p2op and cl>op and cl>p2op
    if name=="Three Inside Down": return p2cl>p2op and pcl<pop and pop<p2cl and pcl>p2op and cl<op and cl<p2op
    if name=="Dragonfly Doji": return body/fr<0.05 and lw>3*body and uw<body*0.1
    if name=="Gravestone Doji": return body/fr<0.05 and uw>3*body and lw<body*0.1
    if name=="Long Legged Doji": return body/fr<0.1 and uw>body and lw>body
    if name=="Belt Hold Bullish": return cl>op and lw<body*0.02 and body/fr>0.7
    if name=="Belt Hold Bearish": return cl<op and uw<body*0.02 and body/fr>0.7
    if name=="Kicker Bullish": return pcl<pop and cl>op and op>pcl
    if name=="Kicker Bearish": return pcl>pop and cl<op and op<pcl
    if name=="Three Outside Up": return p2cl<p2op and cl>op and op<p2cl and cl>p2op and pcl>p2op
    if name=="Three Outside Down": return p2cl>p2op and cl<op and op>p2cl and cl<p2op and pcl<p2op
    if name=="On Neck": return pcl<pop and cl>op and abs(cl-plo)/fr<0.02
    return False

def _ex(df,i):
    c,p,p2=df.iloc[i],df.iloc[i-1],df.iloc[i-2]
    op,hi,lo,cl=c['open'],c['high'],c['low'],c['close']
    pop,phi,plo,pcl=p['open'],p['high'],p['low'],p['close']
    p2op,p2cl=p2['open'],p2['close']
    body=abs(cl-op); fr=hi-lo if hi-lo!=0 else 0.0001
    return op,hi,lo,cl,pop,phi,plo,pcl,p2op,p2cl,body,fr,hi-max(op,cl),min(op,cl)-lo,abs(pcl-pop)

def detect_patterns(df):
    if df is None or len(df)<3: return []
    v=_ex(df,len(df)-1); result=[]
    for name,sentiment in ALL_PATTERNS:
        try:
            if detect_single(name,*v): result.append((name,sentiment,DESCS.get(name,"")))
        except: pass
    return result

def scan_patterns(df,active):
    result={p:{"x":[],"y":[],"sentiment":"neutral"} for p in active}
    if df is None or len(df)<3: return result
    sm={n:s for n,s in ALL_PATTERNS}; offset=(df['high'].max()-df['low'].min())*0.008
    for i in range(2,len(df)):
        v=_ex(df,i)
        for pname in active:
            try:
                if detect_single(pname,*v):
                    s=sm.get(pname,"neutral"); result[pname]["x"].append(df.index[i])
                    result[pname]["y"].append(v[1]+offset if s in ["bearish","neutral"] else v[2]-offset)
                    result[pname]["sentiment"]=s
            except: pass
    return result

def _parse_news_item(item):
    try:
        content=item.get("content",item); title=content.get("title","") or item.get("title","")
        link=""; cp=content.get("canonicalUrl",{})
        if isinstance(cp,dict): link=cp.get("url","")
        if not link: link=content.get("url","") or item.get("link","#")
        prov=content.get("provider",{}); source=(prov.get("displayName","") or prov.get("name","")) if isinstance(prov,dict) else item.get("publisher","")
        ts_str=content.get("pubDate","") or content.get("publishedAt",""); ts_raw=item.get("providerPublishTime",0)
        if ts_str:
            try: dt=datetime.strptime(ts_str[:19],"%Y-%m-%dT%H:%M:%S").strftime("%b %d  %H:%M")
            except: dt=datetime.fromtimestamp(ts_raw).strftime("%b %d  %H:%M") if ts_raw else ""
        else: dt=datetime.fromtimestamp(ts_raw).strftime("%b %d  %H:%M") if ts_raw else ""
        if not title: return None
        return {"title":title,"source":source,"link":link or "#","time":dt}
    except: return None

_NEWS_CACHE = {}
def fetch_category_news(symbols,limit=4):
    key = tuple(symbols)
    now = time.time()
    cached = _NEWS_CACHE.get(key)
    if cached and (now - cached["ts"]) < 300:
        return cached["data"]
    seen=set(); result=[]
    for sym in symbols:
        try:
            for item in (yf.Ticker(sym).news or [])[:limit]:
                p=_parse_news_item(item)
                if p and p["title"] not in seen: seen.add(p["title"]); result.append(p)
        except: pass
    result = result[:6]
    _NEWS_CACHE[key] = {"data": result, "ts": now}
    return result

def render_news_section(cat,items,cat_color,cat_icon):
    if not items: return html.Div()
    cards=[]
    for a in items:
        cards.append(html.A(href=a.get("link","#"),target="_blank",style={"textDecoration":"none"},
            children=html.Div([html.Div(style={"width":"3px","backgroundColor":cat_color,"borderRadius":"2px","marginRight":"10px","flexShrink":"0","marginTop":"2px"}),html.Div([html.Div(a.get("title",""),style={"color":TEXT_MAIN,"fontSize":"0.8em","lineHeight":"1.45","fontWeight":"500","marginBottom":"5px"}),html.Div([html.Span(a.get("source",""),style={"color":cat_color,"fontSize":"0.6em","fontWeight":"600","marginRight":"8px"}),html.Span(a.get("time",""),style={"color":TEXT_MUTED,"fontSize":"0.6em"})])],style={"flex":"1"})],
            className="news-card",style={"display":"flex","alignItems":"flex-start","backgroundColor":"#0a0912","border":f"1px solid {BORDER}","borderRadius":"7px","padding":"10px 12px","marginBottom":"6px","cursor":"pointer"})))
    return html.Div([html.Div([html.Span(cat_icon,style={"color":cat_color,"marginRight":"7px","fontSize":"0.9em"}),html.Span(cat.upper(),style={"color":cat_color,"fontSize":"0.58em","fontWeight":"700","letterSpacing":"1.5px"})],style={"marginBottom":"8px","marginTop":"16px","display":"flex","alignItems":"center"}),html.Div(cards)])


# ── Forex Factory economic calendar (cached, public XML feed) ────────────────
_FF_CACHE = {"data": None, "ts": 0}

def fetch_forex_factory_events(max_events=12):
    """Fetch upcoming economic events from the ForexFactory weekly XML feed.
    Cached for 10 minutes to respect rate limits."""
    now = time.time()
    if _FF_CACHE["data"] is not None and (now - _FF_CACHE["ts"]) < 600:
        return _FF_CACHE["data"]
    try:
        url = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"
        r = http_req.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        if not r.ok:
            return _FF_CACHE["data"] or []
        root = ET.fromstring(r.content)
        events = []
        impact_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢", "Holiday": "⚪"}
        for ev in root.findall("event"):
            def _g(tag):
                n = ev.find(tag)
                return (n.text or "").strip() if n is not None and n.text else ""
            title    = _g("title")
            country  = _g("country")
            date_txt = _g("date")
            time_txt = _g("time")
            impact   = _g("impact") or "Low"
            forecast = _g("forecast")
            previous = _g("previous")
            actual   = _g("actual")
            if not title:
                continue
            # Skip past events — only keep today & upcoming this week
            try:
                ev_dt = datetime.strptime(f"{date_txt} {time_txt}", "%m-%d-%Y %I:%M%p")
                if ev_dt < datetime.now():
                    continue
            except Exception:
                pass
            when = f"{date_txt}  {time_txt}".strip()
            events.append({
                "title":    title,
                "country":  country,
                "impact":   impact,
                "emoji":    impact_emoji.get(impact, "⚪"),
                "when":     when,
                "forecast": forecast,
                "previous": previous,
                "actual":   actual,
            })
        # Prioritise High impact, then chronological
        events.sort(key=lambda e: (0 if e["impact"] == "High" else 1 if e["impact"] == "Medium" else 2))
        events = events[:max_events]
        _FF_CACHE["data"] = events
        _FF_CACHE["ts"]   = now
        return events
    except Exception:
        return _FF_CACHE["data"] or []

def render_forex_factory_section(events):
    if not events:
        return html.Div()
    cards = []
    for ev in events:
        impact_color = {"High": BEAR, "Medium": "#facc15", "Low": BULL, "Holiday": TEXT_MUTED}.get(ev["impact"], TEXT_MUTED)
        detail_bits = []
        if ev["actual"]:   detail_bits.append(f"Actual: {ev['actual']}")
        if ev["forecast"]: detail_bits.append(f"Forecast: {ev['forecast']}")
        if ev["previous"]: detail_bits.append(f"Prev: {ev['previous']}")
        detail_txt = "  ·  ".join(detail_bits) if detail_bits else ""
        cards.append(html.Div([
            html.Div(style={"width":"3px","backgroundColor":impact_color,"borderRadius":"2px","marginRight":"10px","flexShrink":"0","marginTop":"2px"}),
            html.Div([
                html.Div([
                    html.Span(ev["emoji"], style={"marginRight":"6px"}),
                    html.Span(f"{ev['country']}  ·  {ev['title']}", style={"color":TEXT_MAIN,"fontSize":"0.78em","fontWeight":"600"}),
                ], style={"marginBottom":"3px","lineHeight":"1.35"}),
                html.Div([
                    html.Span(ev["when"], style={"color":impact_color,"fontSize":"0.6em","fontWeight":"600","marginRight":"8px"}),
                    html.Span(detail_txt, style={"color":TEXT_MUTED,"fontSize":"0.6em"}),
                ]),
            ], style={"flex":"1"}),
        ], style={"display":"flex","alignItems":"flex-start","backgroundColor":"#0a0912","border":f"1px solid {BORDER}","borderRadius":"7px","padding":"10px 12px","marginBottom":"6px"}))
    return html.Div([
        html.Div([
            html.Span("📅", style={"color":"#f59e0b","marginRight":"7px","fontSize":"0.9em"}),
            html.Span("ECONOMIC CALENDAR  ·  FOREX FACTORY", style={"color":"#f59e0b","fontSize":"0.58em","fontWeight":"700","letterSpacing":"1.5px"}),
        ], style={"marginBottom":"8px","marginTop":"4px","display":"flex","alignItems":"center"}),
        html.Div(cards),
    ])

def build_news_content():
    """Build the full news panel. Wrapped so any single source failing can't crash the callback."""
    sections = []
    # ── Forex Factory calendar first (trader-priority) ──────────────────────
    try:
        ff_events = fetch_forex_factory_events()
        ff_section = render_forex_factory_section(ff_events)
        if ff_events:
            sections.append(ff_section)
    except Exception:
        pass
    # ── Yahoo finance news per category ────────────────────────────────────
    for cat, syms in NEWS_SOURCES.items():
        try:
            items = fetch_category_news(syms)
            sections.append(render_news_section(cat, items, NEWS_CAT_COLORS.get(cat, NEUTRAL), NEWS_CAT_ICONS.get(cat, "●")))
        except Exception:
            continue
    if not sections:
        sections.append(html.Div("News temporarily unavailable. Try refreshing.",
                                 style={"color": TEXT_MUTED, "fontSize": "0.78em", "fontStyle": "italic", "padding": "20px 0"}))
    return sections


