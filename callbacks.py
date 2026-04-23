# ══════════════════════════════════════════════════════════════════════════════
#  callbacks.py  —  Root layout, index_string, and all @app.callback functions
# ══════════════════════════════════════════════════════════════════════════════

import dash
from dash import dcc, html, Input, Output, State, ALL, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

import secrets
from server import app
from config import (
    PURPLE, PURPLE_LIGHT, BG_DARK, BG_CARD, BG_CARD2, BORDER,
    BULL, BEAR, NEUTRAL, TEXT_MAIN, TEXT_DIM, TEXT_MUTED, MA50_COLOR, MA20_COLOR,
    PLAN_LIMITS, REGISTERED_USERS, BETA_ACCOUNTS, ADMIN_EMAIL, ADMIN_PASSWORD,
    ASSET_ICONS, LABELS, SYMBOLS, ALL_OPTIONS, CATEGORY_ICONS,
    ALL_PATTERNS, PAT_COLOR, PAT_ABBR, SEN_EMOJI, SEN_LABEL, DESCS,
    _register_user, _mark_login, call_bojket,
    VERIFIED_ACCOUNTS, PENDING_VERIFICATIONS, EMAIL_ENABLED,
    send_verification_email,
    register_session, unregister_session,
)
from ml import (
    _ML_LOCK, _BT_LOCK, _ML_STATE, _BT_STATE, _ML_MODEL, _ML_SCALER,
    ml_predict, start_ml_training, start_backtest, load_ml_model,
    render_backtest_results, render_feat_importance, _prog_bar, _stat_mini,
    HAS_SKLEARN,
)
from data import (
    fetch_data, get_atr, get_indicators, get_bollinger_bands,
    get_support_resistance, get_prev_day_levels, get_sr_confluence,
    get_ema_trend, get_htf_bias, get_vwap_series, superintelligent_signal,
    get_levels, get_summary, get_streak, calc_pnl,
    detect_patterns, scan_patterns, build_news_content,
)
# (ml imports merged above)
from pages import (
    landing_page, login_page, email_sent_page, onboarding_page,
    for_teams_page, book_call_page,
    pricing_page, dashboard_page,
    make_toggles, make_active_list, lbl, tbtn,
    _typing_bubble, render_chat_messages, render_breakdown,
    trade_entry_modal, build_admin_content, build_admin_analytics,
    ADMIN_PANEL_HIDDEN, ADMIN_PANEL_SHOWN,
    NEWS_PANEL_HIDDEN, NEWS_PANEL_SHOWN,
    BREAKDOWN_HIDDEN, BREAKDOWN_SHOWN,
    AILAB_PANEL_HIDDEN, AILAB_PANEL_SHOWN,
    compute_short_term_forecast, render_forecast_card,
    ONBOARDING_QUESTIONS,
)

from ranks import RANKS, render_rank_badge, get_rank_for_user_email
# ══════════════════════════════════════════════════════════════════════════════
#  ROOT LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

app.layout = html.Div([
    dcc.Location(id="url",refresh=False),
    dcc.Store(id="session-store",data={"logged_in":False,"plan":None,"onboarding_done":False,"ob_step":0,"ob_answers":[],"billing":"monthly","pending_email":""}),
    dcc.Store(id="admin-tab-store",data="members"),
    # Permanent hook used by clientside theme callback (must live in root layout)
    html.Div(id="theme-applier",style={"display":"none"}),
    html.Div(id="zoom-guard-sink",style={"display":"none"}),
    html.Div(id="page-content"),
    html.Div([
        # Login page stubs — login page is NOT the initial render (landing_page is),
        # so these are safe here. suppress_callback_exceptions=True does not suppress
        # Input validation in Dash 2.x, so stubs are required for all dynamic-page Inputs.
        html.Button("",id="login-submit-btn",    n_clicks=0),
        html.Button("",id="login-signup-link",   n_clicks=0),
        html.Button("",id="login-back-btn",      n_clicks=0),
        html.Button("",id="login-logo-btn",      n_clicks=0),
        dcc.Input(id="login-email",    type="email",    value=""),
        dcc.Input(id="login-password", type="password", n_submit=0, value=""),
        html.Div("",id="login-error"),
        html.Button("",id="ob-done-btn",         n_clicks=0),
        html.Button("",id="buy-hustler-btn",     n_clicks=0),
        html.Button("",id="buy-veteran-btn",     n_clicks=0),
        html.Button("",id="signout-btn",         n_clicks=0),
        html.Button("",id="skip-verify-btn",     n_clicks=0),
        html.Div("",id="payment-msg"),
        # Trade modal stubs — kept in root layout so callbacks always find them     
        html.Button("",id="what-is-btn",       n_clicks=0),
        html.Div("",   id="what-is-answer"),
        html.Span("",  id="what-is-arrow"),
        html.Button("",id="confirm-trade-btn", n_clicks=0, style={"display":"none"}),
        html.Button("",id="cancel-trade-btn",  n_clicks=0, style={"display":"none"}),
        dcc.Input(id="pos-size-input",  type="number", value=""),
        dcc.Input(id="custom-tp-input", type="number", value=""),
        dcc.Input(id="custom-sl-input", type="number", value=""),
        html.Div("",id="trade-status"),
        html.Div("",id="trade-status-hint"),
        html.Div("",id="copy-tp-feedback",     style={"display":"none"}),
        html.Div("",id="copy-sl-feedback",     style={"display":"none"}),
        html.Button("",id="alert-close-btn",   n_clicks=0),
        html.Button("",id="alert-dropdown-price-btn", n_clicks=0),
        html.Button("",id="alert-dropdown-mute-btn",  n_clicks=0),
        # Clientside-callback sinks — must live in root layout so they exist on every page
        dcc.Store(id="prev-signal",       data=""),
        dcc.Store(id="chat-scroll-dummy", data=0),
    ],style={"position":"fixed","opacity":"0","pointerEvents":"none","height":"0","overflow":"hidden","zIndex":"-1"}),

])

# ── POLLING JS — pure DOM polling, zero Dash callback machinery ───────────────
# Bypasses window.dash_clientside entirely — no "dc[namespace] is undefined" ever.
_POLLING_JS = """
(function() {
/* ── Rank change detector ── */
    var _lastRankTier = null;
    var _tierOrder = {"BRONZE":1, "SILVER":2, "GOLD":3, "PLATINUM":4, "DIAMOND":5};
    setInterval(function() {
        var badge = document.getElementById('rank-badge');
        if (!badge) return;
        var tierEl = badge.querySelector('div > div:first-child');
        if (!tierEl) return;
        var tier = (tierEl.textContent || '').trim();
        if (!tier) return;
        if (_lastRankTier === null) { _lastRankTier = tier; return; }
        if (tier !== _lastRankTier) {
            var oldR = _tierOrder[_lastRankTier] || 0;
            var newR = _tierOrder[tier]           || 0;
            badge.classList.remove('rank-up-anim','rank-down-anim');
            void badge.offsetWidth; /* reflow so the anim restarts */
            if (newR > oldR)      badge.classList.add('rank-up-anim');
            else if (newR < oldR) badge.classList.add('rank-down-anim');
            _lastRankTier = tier;
        }
    }, 800);
    /* ── Chat auto-scroll: watch scrollHeight, jump on change ── */
    var _lastH = 0;
    setInterval(function() {
        var el = document.getElementById('chat-messages-area');
        if (!el) return;
        if (el.scrollHeight !== _lastH) { _lastH = el.scrollHeight; el.scrollTop = el.scrollHeight; }
    }, 120);

    /* ── Copy TP / SL buttons via event delegation ──
       Fades label back to the copy icon after 1.2s.
       Also resets whenever the TP/SL value text changes (e.g. new symbol). */
    function _bjkResetCopyBtn(btnId, color) {
        var b = document.getElementById(btnId);
        if (!b) return;
        b.innerText = '\u29c9';
        b.style.color = color;
        b.style.fontWeight = 'normal';
        b.style.opacity = '1';
        b.style.transition = 'opacity 0.35s ease';
    }
    document.addEventListener('click', function(e) {
        var t = e.target && e.target.closest ? e.target.closest('#copy-tp-btn') : null;
        if (t) {
            var src = document.getElementById('tp-text');
            if (src) try { navigator.clipboard.writeText(src.innerText || src.textContent || ''); } catch(_) {}
            t.style.transition = 'opacity 0.35s ease';
            t.innerText = '\u2713 Copied!'; t.style.color = '#34d399'; t.style.fontWeight = '700'; t.style.opacity = '1';
            setTimeout(function() { if (t && t.innerText.indexOf('Copied') !== -1) t.style.opacity = '0'; }, 900);
            setTimeout(function() { _bjkResetCopyBtn('copy-tp-btn', '#34d399'); }, 1300);
        }
        t = e.target && e.target.closest ? e.target.closest('#copy-sl-btn') : null;
        if (t) {
            var src2 = document.getElementById('sl-text');
            if (src2) try { navigator.clipboard.writeText(src2.innerText || src2.textContent || ''); } catch(_) {}
            t.style.transition = 'opacity 0.35s ease';
            t.innerText = '\u2713 Copied!'; t.style.color = '#f87171'; t.style.fontWeight = '700'; t.style.opacity = '1';
            setTimeout(function() { if (t && t.innerText.indexOf('Copied') !== -1) t.style.opacity = '0'; }, 900);
            setTimeout(function() { _bjkResetCopyBtn('copy-sl-btn', '#f87171'); }, 1300);
        }
    });
    /* Reset copy buttons whenever the TP/SL numeric text changes (e.g. symbol switch). */
    var _lastTp = '', _lastSl = '';
    setInterval(function() {
        var tp = document.getElementById('tp-text');
        var sl = document.getElementById('sl-text');
        var tpTxt = tp ? (tp.innerText || tp.textContent || '') : '';
        var slTxt = sl ? (sl.innerText || sl.textContent || '') : '';
        if (tpTxt !== _lastTp) { _lastTp = tpTxt; _bjkResetCopyBtn('copy-tp-btn', '#34d399'); }
        if (slTxt !== _lastSl) { _lastSl = slTxt; _bjkResetCopyBtn('copy-sl-btn', '#f87171'); }
    }, 300);

    /* ── Light/dark theme: read theme-applier text, apply class to body ── */
    setInterval(function() {
        var ta = document.getElementById('theme-applier');
        if (!ta) return;
        if ((ta.innerText || ta.textContent || '').trim() === 'light') {
            document.body.classList.add('bojket-light');
        } else {
            document.body.classList.remove('bojket-light');
        }
    }, 250);

    /* ── Signal audio alert ── */
    var _prevSig = '';
    setInterval(function() {
        var el = document.getElementById('signal-text');
        if (!el) return;
        var sig = (el.innerText || el.textContent || '').trim();
        if (sig === _prevSig) return;
        var prev = _prevSig; _prevSig = sig;
        if (!sig) return;
        var buy = sig.indexOf('BUY') !== -1, sell = sig.indexOf('SELL') !== -1;
        var wasBuy = prev.indexOf('BUY') !== -1, wasSell = prev.indexOf('SELL') !== -1;
        if ((buy && !wasBuy) || (sell && !wasSell)) {
            try {
                var AC = window.AudioContext || window.webkitAudioContext;
                var ac = new AC();
                function tone(f,s,d) {
                    var o=ac.createOscillator(), g=ac.createGain();
                    o.connect(g); g.connect(ac.destination);
                    o.frequency.value=f; o.type='sine';
                    g.gain.setValueAtTime(0.14, ac.currentTime+s);
                    g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime+s+d);
                    o.start(ac.currentTime+s); o.stop(ac.currentTime+s+d);
                }
                if (buy)  { tone(660,0,0.15); tone(880,0.18,0.18); tone(1100,0.38,0.25); }
                if (sell) { tone(880,0,0.15); tone(660,0.18,0.18); tone(440,0.38,0.25); }
            } catch(_) {}
        }
    }, 500);

    /* ── Zoom guard: prevent chart from zooming in too tight ── */
    var _CANDLE_MS = {'1m':60000,'5m':300000,'15m':900000,'30m':1800000,
                      '1h':3600000,'2h':7200000,'3h':10800000,'4h':14400000,'1d':86400000};
    setInterval(function() {
        var gd = document.getElementById('candle-chart');
        if (!gd || !gd.layout || !gd.layout.xaxis) return;
        var r = gd.layout.xaxis.range;
        if (!r || r.length < 2) return;
        var t0 = new Date(r[0]).getTime(), t1 = new Date(r[1]).getTime();
        if (isNaN(t0) || isNaN(t1) || t1 <= t0) return;
        var dd = document.getElementById('interval-dropdown');
        var iv = dd ? (dd.value || '1h') : '1h';
        var MIN_MS = (_CANDLE_MS[iv] || 300000) * 8;
        if (t1 - t0 < MIN_MS) {
            var mid=(t0+t1)/2, half=MIN_MS/2;
            try { Plotly.relayout(gd, {'xaxis.range[0]':new Date(mid-half).toISOString(),'xaxis.range[1]':new Date(mid+half).toISOString()}); } catch(_) {}
        }
    }, 300);
})();
"""

# ── LIGHT MODE CSS — injected into <head> via index_string ────────────────────
_LIGHT_CSS = """
/* ═══════════════════════ BOJKET LIGHT MODE ═══════════════════════ */
/* Activated when <body class="bojket-light"> */

/* ── Global body & root ── */
.bojket-light, .bojket-light body,
.bojket-light #_dash-app-content { background-color: #FAFAFA !important; color: #111111 !important; }

/* ── Dark background overrides (hex→rgb, as browsers normalize inline styles) ── */
/* #060608  BG_DARK  */ .bojket-light [style*="rgb(6, 6, 8)"]    { background-color: #FAFAFA !important; }
/* #050508  topbar   */ .bojket-light [style*="rgb(5, 5, 8)"]    { background-color: #F0EEF8 !important; }
/* #0d0d0d  BG_CARD  */ .bojket-light [style*="rgb(13, 13, 13)"] { background-color: #FFFFFF !important; }
/* #0f0e18  BG_CARD2 */ .bojket-light [style*="rgb(15, 14, 24)"] { background-color: #F7F5FF !important; }
/* #080808  chart bg */ .bojket-light [style*="rgb(8, 8, 8)"]    { background-color: #FFFFFF !important; }
/* #0a0912  chat bg  */ .bojket-light [style*="rgb(10, 9, 18)"]  { background-color: #F8F7FC !important; }
/* #060510  panels   */ .bojket-light [style*="rgb(6, 5, 16)"]   { background-color: #EEEAF8 !important; }

/* ── Text color overrides (white/off-white → dark) ── */
/* #ffffff  TEXT_MAIN */ .bojket-light [style*="color: rgb(255, 255, 255)"] { color: #111111 !important; }
/* #e2e0f0  TEXT_DIM  */ .bojket-light [style*="color: rgb(226, 224, 240)"] { color: #3d3a5c !important; }
/* #9d9ab0  TEXT_MUTED*/ .bojket-light [style*="color: rgb(157, 154, 176)"] { color: #7a7896 !important; }
/* literal white keyword */
.bojket-light [style*="color: white"] { color: #111111 !important; }

/* ── Border color overrides ── */
/* #1e1a2e  BORDER    */ .bojket-light [style*="rgb(30, 26, 46)"] { border-color: #DDD9EE !important; }

/* ── Form inputs / selects ── */
.bojket-light input, .bojket-light textarea, .bojket-light select,
.bojket-light .form-control, .bojket-light .form-select {
  background-color: #FFFFFF !important;
  color: #111111 !important;
  border-color: #DDD9EE !important;
}
.bojket-light input::placeholder, .bojket-light textarea::placeholder {
  color: #9590aa !important;
}

/* ── Bootstrap dark buttons → light ── */
.bojket-light .btn-dark, .bojket-light .btn-outline-dark {
  background-color: #F0EEF8 !important;
  border-color: #DDD9EE !important;
  color: #3d3a5c !important;
}
.bojket-light .btn-dark:hover, .bojket-light .btn-outline-dark:hover {
  background-color: #E5E2F5 !important;
}

/* ── Dropdowns ── */
.bojket-light .dropdown-menu {
  background-color: #FFFFFF !important;
  border-color: #DDD9EE !important;
}
.bojket-light .dropdown-item { color: #111111 !important; }
.bojket-light .dropdown-item:hover { background-color: #F0EEF8 !important; }

/* ── Symbol pills ── */
.bojket-light .sym-pill { border-color: #DDD9EE !important; color: #3d3a5c !important; }
.bojket-light .sym-pill:hover { background-color: #EEEBf8 !important; color: #9333EA !important; }

/* ── Overlay panels (news, ailab) ── */
.bojket-light #news-panel  { background-color: #FAFAFA !important; border-color: #DDD9EE !important; }
.bojket-light #ailab-panel { background-color: #FAFAFA !important; border-color: #DDD9EE !important; }

/* ── Chat widget ── */
.bojket-light #chat-panel  { background-color: #F8F7FC !important; border-color: #DDD9EE !important; }

/* ── Scrollbars ── */
.bojket-light ::-webkit-scrollbar-track { background: #F0EEF8; }
.bojket-light ::-webkit-scrollbar-thumb { background: #C8C4E0; border-radius: 4px; }
/* ── Rank badge animations ────────────────────────────────── */
            @keyframes rankPulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.04); }}
            }}
            .rank-badge-pulse {{ animation: rankPulse 2.8s ease-in-out infinite; }}
            .rank-badge-pulse:hover {{ transform: scale(1.06) !important; }}
            @keyframes rankUp {{
                0% {{ transform: scale(1); filter: brightness(1); }}
                20% {{ transform: scale(1.3) rotate(-6deg); filter: brightness(1.6); }}
                40% {{ transform: scale(1.15) rotate(4deg); filter: brightness(1.4); }}
                60% {{ transform: scale(1.25) rotate(-2deg); filter: brightness(1.5); }}
                100% {{ transform: scale(1); filter: brightness(1); }}
            }}
            @keyframes rankDown {{
                0% {{ transform: scale(1); filter: brightness(1); }}
                15% {{ transform: translateY(-4px) scale(1.05); filter: brightness(0.7); }}
                30% {{ transform: translateY(6px) scale(0.92); filter: brightness(0.6); }}
                50% {{ transform: translateY(-2px) scale(0.98); filter: brightness(0.8); }}
                100% {{ transform: scale(1); filter: brightness(1); }}
            }}
            .rank-up-anim {{ animation: rankUp 1.4s ease-out !important; }}
            .rank-down-anim {{ animation: rankDown 1.2s ease-out !important; }}

/* ── Keep intentional signal / accent colors unchanged ── */
/* PURPLE #9333EA, BULL #34d399, BEAR #f87171, NEUTRAL #c084fc are preserved */
"""

app.index_string = f"""<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
        <style>
            * {{ font-family: "Inter", sans-serif !important; }}
            body {{ background-color: #060608 !important; margin: 0; overflow-x: hidden; }}
            ::-webkit-scrollbar {{ width: 4px; height: 4px; }}
            ::-webkit-scrollbar-track {{ background: #0d0d0d; }}
            /* ── MOBILE RESPONSIVE RULES ──────────────────────────────── */
            @media (max-width: 768px) {{
                body {{ font-size: 14px !important; }}
                /* Force any container wider than screen to fit */
                div[style*="width"] {{ max-width: 100vw !important; }}
                /* Stack side-by-side panels vertically */
                div[style*="flex"] {{ flex-wrap: wrap !important; }}
                /* Reduce oversized headings */
                div[style*="font-size: 3"] {{ font-size: 1.6em !important; }}
                div[style*="font-size: 4"] {{ font-size: 1.8em !important; }}
                div[style*="font-size: 5"] {{ font-size: 2em !important; }}
                div[style*="font-size: 6"] {{ font-size: 2.2em !important; }}
                /* Shrink large paddings */
                div[style*="padding: 40"] {{ padding: 16px !important; }}
                div[style*="padding: 60"] {{ padding: 20px !important; }}
                div[style*="padding: 80"] {{ padding: 24px !important; }}
                /* Hide desktop-only panels on phone */
                #pattern-panel, #breakdown-panel, #chat-panel {{ display: none !important; }}
                /* Chart fits screen */
                #candle-chart, #candle-chart > div, .js-plotly-plot {{
                    width: 100% !important; max-width: 100vw !important;
                }}
                /* Buttons: better touch targets */
                button {{ min-height: 40px !important; }}
                /* News/Admin/AI Lab overlay panels: full width on phone */
                #news-panel, #ailab-panel, #admin-panel {{
                    width: 100vw !important; max-width: 100vw !important;
                }}
                /* Trade modal */
                #trade-modal > div {{ width: 92vw !important; max-width: 92vw !important; }}
                /* Topbar compact */
                [id$="topbar"] {{ flex-wrap: wrap !important; padding: 8px !important; }}
            }}
            .Select-control {{ background-color: #0f0e18 !important; border-color: #1e1a2e !important; color: #f1f0f5 !important; }}
            .Select-menu-outer {{ background-color: #0f0e18 !important; border-color: #1e1a2e !important; z-index: 9999 !important; }}
            .Select-option {{ background-color: #0f0e18 !important; color: #c4c0d4 !important; font-size: 0.82em !important; }}
            .Select-option:hover {{ background-color: #1a1530 !important; color: #ffffff !important; }}
            .Select-value-label {{ color: #f1f0f5 !important; font-size: 0.82em !important; }}
            .Select-placeholder {{ color: #6b6880 !important; font-size: 0.82em !important; }}
            .Select-arrow {{ border-top-color: #6b6880 !important; }}
            /* ── Symbol dropdown: Space Grotesk, uppercase, bold ── */
            #symbol-input .Select-value-label,
            #symbol-input .Select-option {{
                font-family: "Space Grotesk", "Inter", sans-serif !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.06em !important;
                font-size: 0.82em !important;
            }}
            #symbol-input .Select-option:hover {{ color: #ffffff !important; }}
            /* ── Interval dropdown: Space Grotesk, bold, no uppercase ── */
            #interval-dropdown .Select-value-label,
            #interval-dropdown .Select-option {{
                font-family: "Space Grotesk", "Inter", sans-serif !important;
                font-weight: 700 !important;
                letter-spacing: 0.04em !important;
                font-size: 0.82em !important;
            }}
            #interval-dropdown .Select-option:hover {{ color: #ffffff !important; }}
            .chat-scroll::-webkit-scrollbar {{ width: 3px; }}
            .chat-scroll::-webkit-scrollbar-thumb {{ background: #2a2040; border-radius: 3px; }}
            .news-panel-scroll::-webkit-scrollbar {{ width: 3px; }}
            .news-panel-scroll::-webkit-scrollbar-thumb {{ background: #2a2040; border-radius: 3px; }}
            .ailab-scroll::-webkit-scrollbar {{ width: 3px; }}
            .ailab-scroll::-webkit-scrollbar-thumb {{ background: #2a2040; border-radius: 3px; }}
            .breakdown-scroll::-webkit-scrollbar {{ width: 3px; }}
            .breakdown-scroll::-webkit-scrollbar-thumb {{ background: #2a2040; border-radius: 3px; }}
            /* ── Chart smoothness: GPU layer + no layout jumps ── */
            .js-plotly-plot {{ contain: layout style; }}
            .js-plotly-plot .plotly .main-svg {{ will-change: transform; }}
            .js-plotly-plot .modebar {{ display: none !important; }}
            .inp {{ background-color: #0a0910; border: 1px solid #2a2040; color: #ffffff;
                   padding: 12px 16px !important; border-radius: 10px; font-size: 14px; outline: none; height: 46px; line-height: 1.5;
                   width: 100%; box-sizing: border-box; transition: border-color 0.2s; }}
            .inp:focus {{ border-color: #9333EA; box-shadow: 0 0 0 3px rgba(147,51,234,0.15); }}
            .plan-card:hover {{ border-color: #9333EA !important; transform: translateY(-6px); }}
            .plan-card {{ transition: all 0.25s ease; }}
            .ob-btn:hover {{ background-color: rgba(147,51,234,0.15) !important; border-color: #9333EA !important; color: #ffffff !important; }}
            .ob-btn {{ transition: all 0.15s ease; }}
            .feature-card:hover {{ border-color: rgba(147,51,234,0.4) !important; background-color: #13101f !important; }}
            .feature-card {{ transition: all 0.2s ease; }}
            .news-card:hover {{ border-color: rgba(147,51,234,0.35) !important; background-color: #0f0c1a !important; }}
            .news-card {{ transition: all 0.15s ease; }}
            .ml-tag {{ display:inline-block; padding:2px 8px; border-radius:20px; font-size:0.62em; font-weight:700; letter-spacing:0.5px; }}
            @keyframes fadeInUp {{ from {{ opacity:0; transform:translateY(16px); }} to {{ opacity:1; transform:translateY(0); }} }}
            @keyframes glow-pulse {{ 0%,100% {{ opacity:0.6; }} 50% {{ opacity:1; }} }}
            @keyframes spin {{ from{{transform:rotate(0deg)}} to{{transform:rotate(360deg)}} }}
            .fade-in {{ animation: fadeInUp 0.45s ease forwards; }}
            /* ── Scroll reveal: opacity 0 → 1 as element enters viewport ── */
            .reveal {{ opacity: 0; transform: translateY(24px); transition: opacity 0.9s ease-out, transform 0.9s ease-out; }}
            .reveal.in-view {{ opacity: 1; transform: translateY(0); }}
            /* ── Floating money symbols (scroll-reactive) ── */
            .money-field {{ position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }}
            .money {{ position: absolute; color: rgba(168,85,247,0.10); font-weight: 900; font-size: 4em; filter: blur(0.3px); transition: transform 0.1s linear; user-select: none; }}
            .money.m1  {{ left:  4%;  top:   8%; font-size: 3.2em; }}
            .money.m2  {{ left: 88%;  top:  14%; font-size: 4.6em; }}
            .money.m3  {{ left: 18%;  top:  32%; font-size: 2.6em; }}
            .money.m4  {{ left: 74%;  top:  44%; font-size: 3.8em; }}
            .money.m5  {{ left:  8%;  top:  62%; font-size: 4.2em; }}
            .money.m6  {{ left: 92%;  top:  72%; font-size: 3em;   }}
            .money.m7  {{ left: 28%;  top:  88%; font-size: 3.4em; }}
            .money.m8  {{ left: 64%;  top:  96%; font-size: 4em;   }}
            .money.m9  {{ left: 42%;  top: 118%; font-size: 2.8em; }}
            .money.m10 {{ left: 82%;  top: 138%; font-size: 3.6em; }}
            .money.m11 {{ left: 12%;  top: 158%; font-size: 4.4em; }}
            .money.m12 {{ left: 56%;  top: 176%; font-size: 3em;   }}
            /* ── Mega CTA hover lift ── */
            .cta-mega:hover {{ transform: translateY(-2px); box-shadow: 0 16px 56px rgba(147,51,234,0.65), 0 0 0 1px rgba(168,85,247,0.8) inset; }}
            /* ── Topbar refinements ── */
            .topbar-icon-btn:hover {{ border-color: rgba(168,85,247,0.45) !important; color:white !important; background-color: rgba(147,51,234,0.08) !important; }}
            .topbar-pill-btn:hover {{ color:white !important; border-color: rgba(168,85,247,0.35) !important; background: rgba(147,51,234,0.06) !important; }}
            .topbar-pill-btn.discord:hover {{ border-color: rgba(88,101,242,0.7) !important; background: linear-gradient(135deg,rgba(88,101,242,0.25),rgba(88,101,242,0.08)) !important; }}
            /* ── Tool buttons (market/journal/news/ailab/bell) hover ── */
            .tool-btn:hover {{ border-color: rgba(168,85,247,0.45) !important; color:white !important; background: rgba(147,51,234,0.1) !important; transform: translateY(-1px); }}
            /* ── Symbol pills hover ── */
            .sym-pill:hover {{ color: white !important; border-color: rgba(168,85,247,0.4) !important; background: rgba(147,51,234,0.08) !important; }}
            /* ── Journal rows subtle hover ── */
            #journal-table tr:hover {{ background-color: rgba(147,51,234,0.04) !important; }}
            /* ── Copy button hover ── */
            #copy-tp-btn:hover {{ background-color: rgba(52,211,153,0.12) !important; border-color: rgba(52,211,153,0.7) !important; }}
            #copy-sl-btn:hover {{ background-color: rgba(248,113,113,0.12) !important; border-color: rgba(248,113,113,0.7) !important; }}
            /* ── Exit & Log button hover ── */
            .exit-log-btn:hover {{ background-color: rgba(248,113,113,0.15) !important; border-color: rgba(248,113,113,0.55) !important; }}            /* ── Tool buttons (market/journal/news/ailab/bell) hover ── */
            .tool-btn:hover {{ border-color: rgba(168,85,247,0.45) !important; color:white !important; background: rgba(147,51,234,0.1) !important; transform: translateY(-1px); }}
            /* ── Symbol pills hover ── */
            .sym-pill:hover {{ color: white !important; border-color: rgba(168,85,247,0.4) !important; background: rgba(147,51,234,0.08) !important; }}
            /* ── Journal rows subtle hover ── */
            #journal-table tr:hover {{ background-color: rgba(147,51,234,0.04) !important; }}
            /* ── Copy button hover ── */
            #copy-tp-btn:hover {{ background-color: rgba(52,211,153,0.12) !important; border-color: rgba(52,211,153,0.7) !important; }}
            #copy-sl-btn:hover {{ background-color: rgba(248,113,113,0.12) !important; border-color: rgba(248,113,113,0.7) !important; }}
            /* ── Exit & Log button hover ── */
            .exit-log-btn:hover {{ background-color: rgba(248,113,113,0.15) !important; border-color: rgba(248,113,113,0.55) !important; }}
             .spinning {{ animation: spin 1.2s linear infinite; display:inline-block; }}
            .hero-glow {{
                position: absolute; width: 900px; height: 900px; border-radius: 50%;
                background: radial-gradient(circle, rgba(147,51,234,0.12) 0%, transparent 65%);
                top: -200px; left: 50%; transform: translateX(-50%); pointer-events: none;
                animation: glow-pulse 4s ease infinite;
            }}
            .cta-primary {{
                background: linear-gradient(135deg, #9333EA, #7C3AED);
                border: none; color: white; border-radius: 12px; font-weight: 700;
                cursor: pointer; letter-spacing: 0.3px;
                box-shadow: 0 4px 24px rgba(147,51,234,0.4), 0 1px 0 rgba(255,255,255,0.1) inset;
                transition: all 0.2s ease;
            }}
            .cta-primary:hover {{ transform: translateY(-2px); box-shadow: 0 8px 32px rgba(147,51,234,0.5); }}
            .cta-secondary {{
                background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15);
                color: rgba(255,255,255,0.85); border-radius: 12px; font-weight: 500;
                cursor: pointer; transition: all 0.2s ease;
            }}
            .cta-secondary:hover {{ background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.3); }}
            .prog-bar-fill {{ height:100%; border-radius:4px; transition: width 0.4s ease; }}
            /* ── Chat typing indicator ── */
            @keyframes typing-dot {{ 0%,60%,100% {{ transform:translateY(0); opacity:0.35; }} 30% {{ transform:translateY(-5px); opacity:1; }} }}
            .typing-dot {{ display:inline-block; width:7px; height:7px; border-radius:50%; background:#9333EA; margin:0 3px; animation:typing-dot 1.1s ease-in-out infinite; }}
            .typing-dot:nth-child(2) {{ animation-delay:0.18s; }}
            .typing-dot:nth-child(3) {{ animation-delay:0.36s; }}
        </style>
        <style>{_LIGHT_CSS}</style>
    </head>
    <body>
        <div id="bojket-loader" style="position:fixed;top:0;left:0;width:100vw;height:100vh;background:#060608;z-index:99999;display:flex;align-items:center;justify-content:center;flex-direction:column;transition:opacity 0.5s ease;">
            <div style="position:relative;width:76px;height:76px;">
                <div style="position:absolute;inset:0;border-radius:50%;border:3px solid rgba(147,51,234,0.15);"></div>
                <div style="position:absolute;inset:0;border-radius:50%;border:3px solid transparent;border-top-color:#9333EA;border-right-color:#A855F7;animation:spin 0.9s linear infinite;box-shadow:0 0 30px rgba(147,51,234,0.4);"></div>
            </div>
            <div style="margin-top:26px;color:#A855F7;font-family:Inter,sans-serif;font-weight:900;letter-spacing:6px;font-size:0.9em;">BOJKET</div>
            <div style="margin-top:4px;color:rgba(255,255,255,0.35);font-family:Inter,sans-serif;font-style:italic;font-size:0.7em;letter-spacing:1px;">The future of trading.</div>
        </div>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
        <script>
        /* ── Login form JS bridge ─────────────────────────────────────────────
           The visible login form uses lv-* IDs (no Dash callbacks).
           This bridge proxies user interactions to the hidden stub components
           (login-submit-btn, login-email, login-password, etc.) so that
           Dash callbacks fire from the stubs only — eliminating duplicate IDs.
        ── */
        function _bjkSetReactVal(el, val) {{
            try {{
                var setter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value').set;
                setter.call(el, val);
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }} catch(e) {{}}
        }}
        function _bjkProxyLogin() {{
            var lvEmail  = document.getElementById('lv-email');
            var lvPass   = document.getElementById('lv-password');
            var sEmail   = document.getElementById('login-email');
            var sPass    = document.getElementById('login-password');
            var sBtn     = document.getElementById('login-submit-btn');
            if (lvEmail && sEmail) _bjkSetReactVal(sEmail, lvEmail.value || '');
            if (lvPass  && sPass)  _bjkSetReactVal(sPass,  lvPass.value  || '');
            if (sBtn) sBtn.click();
            /* mirror error message back to visible form after callback fires */
            setTimeout(function() {{
                var sErr = document.getElementById('login-error');
                var vErr = document.getElementById('lv-error');
                if (sErr && vErr) vErr.textContent = sErr.textContent || '';
            }}, 400);
        }}
        document.addEventListener('click', function(e) {{
            var t = e.target;
            if (!t) return;
            /* submit button */
            if (t.id === 'lv-submit' || (t.closest && t.closest('#lv-submit'))) {{
                _bjkProxyLogin();
            }}
            /* signup / view plans link */
            if (t.id === 'lv-signup' || (t.closest && t.closest('#lv-signup'))) {{
                var s = document.getElementById('login-signup-link');
                if (s) s.click();
            }}
            /* back arrow */
            if (t.id === 'lv-back') {{
                var b = document.getElementById('login-back-btn');
                if (b) b.click();
            }}
            /* logo */
            if (t.id === 'lv-logo') {{
                var l = document.getElementById('login-logo-btn');
                if (l) l.click();
            }}
        }});
        document.addEventListener('keydown', function(e) {{
            if (e.key !== 'Enter') return;
            var id = e.target && e.target.id;
            if (id === 'lv-email' || id === 'lv-password') _bjkProxyLogin();
        }});

        /* Video is now a YouTube iframe — no JS injection needed */

        /* ── Money symbols parallax: each one drifts at its own speed ── */
        (function() {{
            var speeds = [0.12, -0.22, 0.18, -0.14, 0.26, -0.18, 0.2, -0.26, 0.14, -0.2, 0.22, -0.16];
            var drifts = [];
            function bind() {{
                drifts = [];
                var items = document.querySelectorAll('.money');
                items.forEach(function(el, i) {{ drifts.push({{el: el, sp: speeds[i % speeds.length]}}); }});
            }}
            function onScroll() {{
                var y = window.scrollY || window.pageYOffset;
                for (var i = 0; i < drifts.length; i++) {{
                    var d = drifts[i];
                    var ty = y * d.sp;
                    d.el.style.transform = 'translateY(' + ty.toFixed(1) + 'px)';
                }}
            }}
            if (document.readyState === 'complete') bind();
            else window.addEventListener('load', bind);
            setInterval(bind, 1500); /* re-bind if Dash swapped the landing */
            window.addEventListener('scroll', onScroll, {{ passive: true }});
        }})();

        /* ── Scroll reveal observer — fade in elements as they enter viewport ── */
        (function() {{
            function bindReveal() {{
                var els = document.querySelectorAll('.reveal:not(.reveal-bound)');
                if (!els.length) return;
                var obs = new IntersectionObserver(function(entries) {{
                    entries.forEach(function(e) {{
                        if (e.isIntersecting) {{
                            e.target.classList.add('in-view');
                            obs.unobserve(e.target);
                        }}
                    }});
                }}, {{ threshold: 0.12, rootMargin: '0px 0px -60px 0px' }});
                els.forEach(function(el) {{ el.classList.add('reveal-bound'); obs.observe(el); }});
            }}
            bindReveal();
            setInterval(bindReveal, 600); /* re-bind when Dash re-renders the page */
        }})();

        /* ── Bojket loader: shows on first paint + on every navigation to /dashboard ── */
        (function() {{
            var loader = document.getElementById('bojket-loader');
            function showLoader() {{
                if (!loader) loader = document.getElementById('bojket-loader');
                if (!loader) return;
                loader.style.display = 'flex';
                /* Next frame so transition fires */
                requestAnimationFrame(function() {{ loader.style.opacity = '1'; }});
            }}
            function hideLoaderSoon() {{
                if (!loader) loader = document.getElementById('bojket-loader');
                if (!loader) return;
                loader.style.opacity = '0';
                setTimeout(function() {{ loader.style.display = 'none'; }}, 500);
            }}
            function dashboardIsFullyLoaded() {{
                /* Dashboard is ready only when the chart canvas has rendered */
                var chart = document.getElementById('live-chart');
                if (!chart) return false;
                var svg = chart.querySelector('.main-svg');
                return !!svg;
            }}
            function initialHide() {{
                var content = document.getElementById('page-content');
                if (!content || content.children.length === 0) {{
                    return setTimeout(initialHide, 100);
                }}
                /* If this is the dashboard route, wait for chart; else hide now. */
                if (window.location.pathname === '/dashboard') {{
                    if (dashboardIsFullyLoaded()) hideLoaderSoon();
                    else setTimeout(initialHide, 150);
                }} else {{
                    hideLoaderSoon();
                }}
            }}
            /* Safety: force-hide after 10s no matter what */
            setTimeout(hideLoaderSoon, 10000);
            if (document.readyState === 'complete') initialHide();
            else window.addEventListener('load', initialHide);

            /* Re-show loader on ANY navigation click heading to /dashboard */
            document.addEventListener('click', function(e) {{
                var a = e.target && e.target.closest ? e.target.closest('a') : null;
                if (a && a.href && a.href.indexOf('/dashboard') !== -1) {{
                    showLoader();
                    /* Watch for dashboard to finish, then hide */
                    var tries = 0;
                    (function wait() {{
                        tries++;
                        if (dashboardIsFullyLoaded()) hideLoaderSoon();
                        else if (tries < 80) setTimeout(wait, 150);
                        else hideLoaderSoon();
                    }})();
                }}
            }}, true);
        }})();

        /* ── Bojket polling JS — pure DOM, no Dash callback machinery ── */
        {_POLLING_JS}
        </script>
    </body>
</html>
"""
# ── "What is Bojket?" click-to-reveal ─────────────────────────────────────────
@app.callback(
    Output("what-is-answer", "style"),
    Output("what-is-arrow", "style"),
    Input("what-is-btn", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_what_is(n):
    if n and n % 2 == 1:
        open_style = {
            "maxHeight":"800px","overflow":"hidden","opacity":"1",
            "transition":"max-height 0.7s ease, opacity 0.7s ease",
            "maxWidth":"1000px","margin":"0 auto",
        }
        arrow_style = {"transition":"transform 0.3s ease","display":"inline-block","transform":"rotate(90deg)"}
        return open_style, arrow_style
    closed_style = {
        "maxHeight":"0","overflow":"hidden","opacity":"0",
        "transition":"max-height 0.7s ease, opacity 0.7s ease",
        "maxWidth":"1000px","margin":"0 auto",
    }
    arrow_style = {"transition":"transform 0.3s ease","display":"inline-block","transform":"rotate(0deg)"}
    return closed_style, arrow_style

# ── PAGE ROUTER ───────────────────────────────────────────────────────────────
@app.callback(
    Output("page-content","children"),
    Input("url","pathname"),
    Input("url","search"),
    Input("session-store","data"),
)
def render_page(path,search,session):
    # Don't re-render the full dashboard on every session change (would reset chart/state)
    trig_id = (dash.callback_context.triggered[0]["prop_id"] if dash.callback_context.triggered else "")
    if "session-store" in trig_id and (path or "/") == "/dashboard":
        return dash.no_update
    logged_in=session.get("logged_in",False)
    ob_done=session.get("onboarding_done",False)
    ob_step=session.get("ob_step",0)
    billing=session.get("billing","monthly")
    plan=session.get("plan")
    pending_email=session.get("pending_email","")

    if path=="/verify":
        token=""
        if search:
            for part in search.lstrip("?").split("&"):
                if part.startswith("token="): token=part[6:]
        if token and token in PENDING_VERIFICATIONS:
            email=PENDING_VERIFICATIONS.pop(token)
            VERIFIED_ACCOUNTS.add(email)
            return html.Div([html.Div([
                html.Div("✅",style={"fontSize":"3em","marginBottom":"16px"}),
                html.Div("Account activated!",style={"color":"white","fontWeight":"800","fontSize":"2em","marginBottom":"10px"}),
                html.Div("Your account is ready. Choose a plan to get started.",style={"color":"rgba(255,255,255,0.5)","fontSize":"0.95em","marginBottom":"28px"}),
            ],style={"textAlign":"center","maxWidth":"460px"})],
            style={"display":"flex","justifyContent":"center","alignItems":"center","minHeight":"100vh","backgroundColor":BG_DARK,"color":TEXT_MAIN})
        return landing_page()

    if path=="/email-sent": return email_sent_page(pending_email)
    if path=="/dashboard":
        if not logged_in: return login_page()
        if not ob_done: return onboarding_page(ob_step,session.get("ob_answers",[]))
        # Handle return from Stripe — plan granted via URL params
        if search and "post_payment=1" in search:
            params = dict(p.split("=",1) for p in search.lstrip("?").split("&") if "=" in p)
            pp = params.get("plan", plan or "hustler")
            return dashboard_page(pp)
        if plan is None: return pricing_page(billing)
        return dashboard_page(plan)
    elif path=="/login":       return login_page()
    elif path=="/for-teams":   return for_teams_page()
    elif path=="/book-call":   return book_call_page()
    elif path=="/pricing":
        # URL search param takes precedence (set by billing toggle links)
        pg_billing = "annual" if (search and "billing=annual" in search) else "monthly"
        return pricing_page(pg_billing)
    elif path=="/onboarding":
        if not logged_in: return login_page()
        return onboarding_page(ob_step,session.get("ob_answers",[]))
    else:
        return landing_page()

# ── POST-PAYMENT: update session-store when returning from Stripe ─────────────
@app.callback(
    Output("session-store","data",allow_duplicate=True),
    Input("url","search"),
    State("session-store","data"),
    prevent_initial_call=True,
)
def handle_post_payment(search, session):
    if not search or "post_payment=1" not in search:
        return dash.no_update
    params = dict(p.split("=",1) for p in search.lstrip("?").split("&") if "=" in p)
    plan    = params.get("plan",    "hustler")
    billing = params.get("billing", "monthly")
    email   = params.get("email",   session.get("pending_email",""))
    s = dict(session)
    s.update({"logged_in": True, "plan": plan, "billing": billing,
              "onboarding_done": True, "pending_email": email})
    if email:
        _register_user(email, plan, billing)
    return s

# ── NAVIGATION ────────────────────────────────────────────────────────────────
@app.callback(
    Output("url","pathname"),
    Output("session-store","data"),
    Input("login-submit-btn","n_clicks"),
    Input("login-password","n_submit"),
    Input("login-signup-link","n_clicks"),
    Input("login-back-btn","n_clicks"),
    Input("login-logo-btn","n_clicks"),
    Input({"type":"ob-answer","index":ALL},"n_clicks"),
    Input("ob-done-btn","n_clicks"),
    Input("buy-hustler-btn","n_clicks"),
    Input("buy-veteran-btn","n_clicks"),
    Input("signout-btn","n_clicks"),
    Input("skip-verify-btn","n_clicks"),
    State("session-store","data"),
    State("login-email","value"),
    State("login-password","value"),
    State("url","pathname"),
    State("url","search"),
    prevent_initial_call=True
)
def handle_navigation(login_sub,login_enter,signup_link,back_btn,logo_btn,ob_ans,ob_done,buy_h,buy_v,signout,skip_verify,session,email,password,current_path,url_search):
    trig=dash.callback_context.triggered[0]["prop_id"]; s=dict(session)
    if any(x in trig for x in ["login-back-btn","login-logo-btn"]): return "/",s
    if "login-signup-link" in trig: return "/pricing",s
    if any(x in trig for x in ["login-submit-btn","login-password"]):
        e=(email or "").strip().lower(); p=(password or "").strip()
        if e==ADMIN_EMAIL.lower() and p==ADMIN_PASSWORD:
            sid = secrets.token_urlsafe(16)
            s.update({"logged_in":True,"plan":"admin","onboarding_done":True,"pending_email":"","session_id":sid})
            return "/dashboard",s
        if e in BETA_ACCOUNTS and p==BETA_ACCOUNTS[e]:
            sid = secrets.token_urlsafe(16)
            if not register_session(e, sid):
                return dash.no_update, s
            _register_user(e,"veteran","monthly")
            _mark_login(e)
            s.update({"logged_in":True,"plan":"veteran","onboarding_done":True,"pending_email":e,"session_id":sid})
            return "/dashboard",s
        if e and p and len(p)>=6:
            if e in VERIFIED_ACCOUNTS or not EMAIL_ENABLED:
                sid = secrets.token_urlsafe(16)
                if not register_session(e, sid):
                    return dash.no_update, s
                _mark_login(e)
                s.update({"logged_in":True,"plan":None,"onboarding_done":False,"ob_step":0,"ob_answers":[],"pending_email":e,"session_id":sid})
                return "/onboarding",s
            else:
                token=secrets.token_urlsafe(32); PENDING_VERIFICATIONS[token]=e
                send_verification_email(e,token); s["pending_email"]=e
                return "/email-sent",s
        return dash.no_update,s
    if "skip-verify-btn" in trig:
        e=s.get("pending_email","demo@bojket.com"); VERIFIED_ACCOUNTS.add(e)
        s.update({"logged_in":True,"plan":None,"onboarding_done":False,"ob_step":0,"ob_answers":[],"pending_email":e})
        return "/onboarding",s
    if "ob-answer" in trig:
        step=s.get("ob_step",0); answers=list(s.get("ob_answers",[])); answers.append(step)
        next_step=step+1; s.update({"ob_step":next_step,"ob_answers":answers})
        if next_step>=len(ONBOARDING_QUESTIONS): s["onboarding_done"]=True
        return "/onboarding",s
    if "ob-done-btn"     in trig: return "/pricing",s
    if "buy-hustler-btn" in trig:
        billing = "annual" if (url_search and "billing=annual" in url_search) else "monthly"
        email   = s.get("pending_email", "")
        return f"/create-checkout-session?plan=hustler&billing={billing}&email={email}", s
    if "buy-veteran-btn" in trig:
        billing = "annual" if (url_search and "billing=annual" in url_search) else "monthly"
        email   = s.get("pending_email", "")
        return f"/create-checkout-session?plan=veteran&billing={billing}&email={email}", s
    if "signout-btn"         in trig:
        unregister_session(s.get("pending_email",""), s.get("session_id",""))
        return "/",{"logged_in":False,"plan":None,"onboarding_done":False,"ob_step":0,"ob_answers":[],"billing":"monthly","pending_email":"","session_id":""}
    return dash.no_update,s

@app.callback(Output("login-error","children"),Input("login-submit-btn","n_clicks"),Input("login-password","n_submit"),State("login-email","value"),State("login-password","value"),prevent_initial_call=True)
def login_error(n,ns,email,password):
    e=(email or "").strip(); p=(password or "").strip()
    if not e: return "Please enter your email."
    if not p: return "Please enter your password."
    if len(p)<6: return "Password must be at least 6 characters."
    from config import ACTIVE_SESSIONS, MAX_DEVICES
    if len(ACTIVE_SESSIONS.get(e.strip().lower(), set())) >= MAX_DEVICES:
        return "⚠️ This account is already signed in on another device. Sign out there first."
    return ""

# ── LANGUAGE CALLBACKS ────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD CALLBACKS
# ══════════════════════════════════════════════════════════════════════════════


def _toggle(style):
    on=style.get("display")=="block"
    return {"display":"none"} if on else {"display":"block","padding":"14px 24px"}

@app.callback(Output("market-panel","style"),  Input("market-btn","n_clicks"),  State("market-panel","style"),  prevent_initial_call=True)
def tog_market(n,s): return _toggle(s)
_PAT_SIDEBAR_HIDDEN={"display":"none"}
_PAT_SIDEBAR_SHOWN={"display":"block","width":"170px","flexShrink":"0","backgroundColor":"#07060f",
    "border":f"1px solid {BORDER}","borderRadius":"10px","overflowY":"auto",
    "maxHeight":"680px","alignSelf":"flex-start","position":"sticky","top":"0"}
@app.callback(Output("pattern-panel","style"), Input("pattern-btn","n_clicks"), State("pattern-panel","style"), prevent_initial_call=True)
def tog_patterns(n,s): return _PAT_SIDEBAR_HIDDEN if s.get("display")=="block" else _PAT_SIDEBAR_SHOWN
@app.callback(Output("journal-panel","style"), Input("journal-btn","n_clicks"), State("journal-panel","style"), prevent_initial_call=True)
def tog_journal(n,s): return _toggle(s)
# ── Rank badge live update ────────────────────────────────────────────────────
@app.callback(
    Output("rank-badge-container", "children"),
    Input("trade-store", "data"),
    Input("journal-store", "data"),
    State("session-store", "data"),
    prevent_initial_call=False,
)
def update_rank_badge(trade_store, journal, session):
    email = (session or {}).get("pending_email", "")
    if email and email in REGISTERED_USERS:
        trades = REGISTERED_USERS[email].get("trades", [])
    else:
        trades = journal or []
    from ranks import get_rank
    rank = get_rank(trades)
    return [render_rank_badge(rank)]
# ── Bell dropdown open/close ──────────────────────────────────────────────────
@app.callback(
    Output("bell-dd-store","data"),
    Input("alert-btn","n_clicks"),
    Input("alert-dropdown-price-btn","n_clicks"),
    Input("alert-dropdown-mute-btn","n_clicks"),
    State("bell-dd-store","data"),
    prevent_initial_call=True,
)
def toggle_bell_dropdown(bell_n, price_n, mute_n, is_open):
    trig = dash.callback_context.triggered[0]["prop_id"]
    if "alert-btn" in trig:
        return not is_open          # toggle on bell click
    return False                    # close on any option click

# ── Dropdown visibility + bell icon/style + mute label from stores ────────────
@app.callback(
    Output("alert-dropdown","style"),
    Output("alert-btn","children"),
    Output("alert-btn","style"),
    Output("alert-dropdown-mute-btn","children"),
    Input("bell-dd-store","data"),
    Input("mute-store","data"),
    prevent_initial_call=True,
)
def update_bell_ui(dd_open, muted):
    dd_style = {
        "display": "block" if dd_open else "none",
        "position":"absolute","top":"calc(100% + 8px)","left":"0",
        "backgroundColor":"#0f0e18","border":"1px solid rgba(255,255,255,0.14)",
        "borderRadius":"10px","padding":"5px","minWidth":"188px","zIndex":"600",
        "boxShadow":"0 8px 32px rgba(0,0,0,0.7)",
    }
    if muted:
        icon      = "🔕"
        btn_style = {
            "border":"1px solid rgba(248,113,113,0.6)","color":"#f87171",
            "backgroundColor":"rgba(248,113,113,0.08)","padding":"5px 11px",
            "fontSize":"0.85em","borderRadius":"6px","cursor":"pointer","minWidth":"0",
        }
        mute_label = [html.Span("🔔", style={"marginRight":"8px"}), "Unmute Notifications"]
    else:
        icon      = "🔔"
        btn_style = {
            "border":"1px solid rgba(255,255,255,0.22)","color":"rgba(255,255,255,0.72)",
            "backgroundColor":"transparent","padding":"5px 11px",
            "fontSize":"0.85em","borderRadius":"6px","cursor":"pointer","minWidth":"0",
        }
        mute_label = [html.Span("🔕", style={"marginRight":"8px"}), "Mute Notifications"]
    return dd_style, icon, btn_style, mute_label

# ── "Set Price Alert" option + close button → show/hide floating card ─────────
_ALERT_SHOWN  = {"display":"block","position":"fixed","top":"62px","right":"230px","width":"280px",
                 "backgroundColor":"#0d0c1a","border":"1px solid rgba(147,51,234,0.45)",
                 "borderRadius":"14px","padding":"18px 20px","zIndex":"500",
                 "boxShadow":"0 16px 48px rgba(0,0,0,0.75), 0 0 0 1px rgba(147,51,234,0.1)"}
_ALERT_HIDDEN = {**_ALERT_SHOWN, "display":"none"}

@app.callback(
    Output("alert-panel","style"),
    Input("alert-dropdown-price-btn","n_clicks"),
    Input("alert-close-btn","n_clicks"),
    State("alert-panel","style"),
    prevent_initial_call=True,
)
def open_alert_panel(open_n, close_n, s):
    trig = dash.callback_context.triggered[0]["prop_id"]
    if "alert-close-btn" in trig:
        return _ALERT_HIDDEN
    return _ALERT_SHOWN if s.get("display") != "block" else _ALERT_HIDDEN

# ── "Mute" option → toggle mute store ────────────────────────────────────────
@app.callback(
    Output("mute-store","data"),
    Input("alert-dropdown-mute-btn","n_clicks"),
    State("mute-store","data"),
    prevent_initial_call=True,
)
def toggle_mute(n, muted):
    return not muted
@app.callback(Output("chart-theme","data"),    Input("theme-btn","n_clicks"),   State("chart-theme","data"),    prevent_initial_call=True)
def tog_theme(n,t): return "light" if t=="dark" else "dark"

# ── FULL-APP LIGHT / DARK MODE ────────────────────────────────────────────────
# Python callback writes theme string to theme-applier div;
# polling JS in index_string reads it and applies/removes class on <body>.
@app.callback(Output("theme-applier","children"), Input("chart-theme","data"))
def _sync_theme(t): return t or "dark"

# ── Zoom guard handled by polling JS in index_string ──────────────────────────

# ── Copy TP / SL handled by event delegation in polling JS ────────────────────


# Python callback: update the theme button icon (safe — no emoji in JS)
@app.callback(Output("theme-btn","children",allow_duplicate=True),
              Input("chart-theme","data"), prevent_initial_call=True)
def update_theme_icon(theme):
    return "\u2600\ufe0f" if theme == "light" else "\U0001f319"   # ☀️ or 🌙
@app.callback(Output("bb-store","data"),       Input("bb-btn","n_clicks"),      State("bb-store","data"),       prevent_initial_call=True)
def tog_bb(n,d): return not d
@app.callback(Output("pd-store","data"),       Input("pd-btn","n_clicks"),      State("pd-store","data"),       prevent_initial_call=True)
def tog_pd(n,d): return not d

@app.callback(Output("trade-modal","children"),Output("trade-modal","style"),Output("pending-trade-store","data"),Input("i-bought-btn","n_clicks"),Input("cancel-trade-btn","n_clicks"),State("trade-store","data"),State("symbol-input","value"),State("interval-dropdown","value"),State("session-store","data"),prevent_initial_call=True)
def open_trade_modal(buy_clicks,cancel_clicks,trade_store,symbol,interval,session):
    trig=dash.callback_context.triggered[0]["prop_id"]; hidden={"display":"none"}
    if "cancel-trade-btn" in trig and cancel_clicks:
        return [],hidden,None
    if "i-bought-btn" in trig and buy_clicks:
        period_map={"1m":"5d","5m":"5d","15m":"1mo","30m":"1mo","1h":"3mo","2h":"6mo","3h":"6mo","4h":"6mo","1d":"2y"}
        df=fetch_data((symbol or "BTC-USD").upper().strip(),interval=interval or "5m",period=period_map.get(interval or "5m","5d"))
        if df is None or df.empty:
            return dash.no_update, dash.no_update, dash.no_update
        plan=session.get("plan","hustler"); patterns=detect_patterns(df)
        signal,_,_,_,_=superintelligent_signal(df,symbol or "BTC-USD",interval or "5m",patterns,plan)
        if signal=="WAIT": signal="BUY"
        entry,default_tp,default_sl=get_levels(df,signal)
        atr=get_atr(df)
        if entry is None:
            entry=float(df['close'].iloc[-1])
            default_tp=entry*1.02 if signal=="BUY" else entry*0.98
            default_sl=entry*0.99 if signal=="BUY" else entry*1.01
        pending={"signal":signal,"entry":entry,"default_tp":default_tp,"default_sl":default_sl,"symbol":symbol,"atr":atr}
        return trade_entry_modal(signal,entry,default_tp,default_sl,atr),{"display":"block"},pending
    return dash.no_update, dash.no_update, dash.no_update

@app.callback(Output("news-panel","style"),Output("news-content","children"),Output("news-last-updated","children"),Input("news-btn","n_clicks"),Input("news-close-btn","n_clicks"),Input("news-refresh-btn","n_clicks"),State("news-panel","style"),prevent_initial_call=True)
def toggle_news(o,c,r,style):
    trig=dash.callback_context.triggered[0]["prop_id"]; is_open=style.get("display")!="none"
    if "news-close-btn" in trig: return NEWS_PANEL_HIDDEN,dash.no_update,dash.no_update
    if "news-btn" in trig and is_open: return NEWS_PANEL_HIDDEN,dash.no_update,dash.no_update
    return NEWS_PANEL_SHOWN,build_news_content(),f"Updated {datetime.now().strftime('%H:%M')}"
@app.callback(Output("symbol-input","value"),Input({"type":"sym-btn","index":ALL},"n_clicks"),prevent_initial_call=True)
def pick_symbol(n):
    t=dash.callback_context.triggered
    if not t or t[0]["value"] is None: return dash.no_update
    try: return json.loads(t[0]["prop_id"].split(".")[0])["index"]
    except: return dash.no_update

@app.callback(Output("active-patterns-store","data"),Output("pattern-toggle-container","children"),Output("active-pattern-list","children"),Input({"type":"pat-toggle","index":ALL},"n_clicks"),State("active-patterns-store","data"),State("session-store","data"),prevent_initial_call=True)
def tog_pat(_,active,session):
    tid=ctx.triggered_id
    if not tid: return active,make_toggles(active),make_active_list(active)
    plan=session.get("plan","hustler"); limits=PLAN_LIMITS.get(plan,PLAN_LIMITS[None])
    max_pat=limits["max_patterns"]; name=tid["index"]
    if name in active: active=[x for x in active if x!=name]
    elif len(active)<max_pat: active=active+[name]
    return active,make_toggles(active,max_pat),make_active_list(active)

@app.callback(Output("alert-store","data"),Output("alert-status","children"),Input("set-alert-btn","n_clicks"),Input("clear-alert-btn","n_clicks"),State("alert-input","value"),State("alert-store","data"),prevent_initial_call=True)
def set_alert(sn,cn,price,store):
    trig=dash.callback_context.triggered[0]["prop_id"]
    if "clear" in trig: return {"price":None,"active":False},"Alert cleared"
    if price: return {"price":float(price),"active":True},f"Alert set at {price}"
    return store,"Enter a price first"

@app.callback(
    Output("trade-store","data"),
    Output("trade-modal","style",allow_duplicate=True),
    Output("trade-modal","children",allow_duplicate=True),
    Output("journal-store","data"),
    Input("confirm-trade-btn","n_clicks"),
    Input("exit-btn","n_clicks"),
    State("pending-trade-store","data"),
    State("trade-store","data"),
    State("journal-store","data"),
    State("pos-size-input","value"),
    State("custom-tp-input","value"),
    State("custom-sl-input","value"),
    State("trade-status","children"),
    State("session-store","data"),
    prevent_initial_call=True,
)
@app.callback(
    Output("trade-store","data"),
    Output("trade-modal","style",allow_duplicate=True),
    Output("trade-modal","children",allow_duplicate=True),
    Input("confirm-trade-btn","n_clicks"),
    State("pending-trade-store","data"),
    State("trade-store","data"),
    State("pos-size-input","value"),
    State("custom-tp-input","value"),
    State("custom-sl-input","value"),
    prevent_initial_call=True,
)
def confirm_trade(confirm_n, pending, store, pos_size, custom_tp, custom_sl):
    if not confirm_n or not pending:
        return dash.no_update, dash.no_update, dash.no_update
    store = store or {}
    try: tp = float(custom_tp) if custom_tp else pending.get("default_tp")
    except: tp = pending.get("default_tp")
    try: sl = float(custom_sl) if custom_sl else pending.get("default_sl")
    except: sl = pending.get("default_sl")
    try: ps = float(pos_size) if pos_size else None
    except: ps = None
    new_store = {
        "in_trade": True, "entry": pending.get("entry"),
        "signal": pending.get("signal","BUY"), "symbol": pending.get("symbol","?"),
        "time": datetime.now().strftime("%H:%M"), "position_size": ps,
        "custom_tp": tp, "custom_sl": sl, "tp": tp, "sl": sl,
        "cooldown": False, "cooldown_since": None,
        "last_result": store.get("last_result"),
        "consecutive_losses": store.get("consecutive_losses", 0),
    }
    return new_store, {"display":"none"}, []


@app.callback(
    Output("trade-store","data",allow_duplicate=True),
    Output("journal-store","data"),
    Input("exit-btn","n_clicks"),
    State("trade-store","data"),
    State("journal-store","data"),
    State("trade-status","children"),
    State("session-store","data"),
    prevent_initial_call=True,
)
def exit_trade(n, store, journal, status, session):
    if not n:
        return dash.no_update, dash.no_update
    store = store or {}
    journal = journal or []
    if not store.get("in_trade"):
        return dash.no_update, dash.no_update
    if isinstance(status, str) and status not in ["-", "Active", "—", "Monitoring..."]:
        result = status
    else:
        result = "Manual exit"
    is_win = "TP" in str(result)
    if is_win: new_losses = 0
    elif "SL" in str(result): new_losses = store.get("consecutive_losses", 0) + 1
    else: new_losses = store.get("consecutive_losses", 0)
    trade_entry = {
        "symbol": store.get("symbol","?"), "signal": store.get("signal","?"),
        "entry": store.get("entry","?"), "size": store.get("position_size","?"),
        "tp": store.get("tp","?"), "sl": store.get("sl","?"),
        "in": store.get("time","?"), "out": datetime.now().strftime("%H:%M"),
        "result": result, "date": datetime.now().strftime("%d %b %Y"),
    }
    new_journal = journal + [trade_entry]
    email = (session or {}).get("pending_email", "")
    if email and email in REGISTERED_USERS:
        REGISTERED_USERS[email].setdefault("trades", []).append(trade_entry)
        REGISTERED_USERS[email]["last_trade"] = datetime.now().strftime("%d %b %Y  %H:%M")
    new_store = {
        "in_trade": False, "entry": None, "signal": None, "symbol": None,
        "time": None, "position_size": None, "custom_tp": None, "custom_sl": None,
        "tp": None, "sl": None, "cooldown": True,
        "cooldown_since": datetime.now().isoformat(),
        "last_result": result, "consecutive_losses": new_losses,
    }
    return new_store, new_journal

@app.callback(Output("journal-table","children"),Output("streak-display","children"),Input("journal-store","data"))
def render_journal(journal):
    streak=get_streak(journal)
    if streak>=3: streak_el=html.Div([html.Span("🔥",style={"marginRight":"6px"}),html.Span(f"{streak} TP streak",style={"color":BULL,"fontWeight":"600","fontSize":"0.82em"}),html.Span(" — signals are running hot",style={"color":TEXT_MUTED,"fontSize":"0.75em","fontStyle":"italic"})],style={"marginBottom":"10px"})
    elif streak>0: streak_el=html.Div(f"✅  {streak} consecutive TP hit{'s' if streak>1 else ''}",style={"color":BULL,"fontSize":"0.78em","marginBottom":"8px"})
    else: streak_el=html.Div("")
    if not journal: return html.Div("No trades logged yet.",style={"color":TEXT_MUTED,"fontSize":"0.78em","fontStyle":"italic","padding":"4px 0"}),streak_el
    headers=["SYMBOL","SIGNAL","SIZE","ENTRY","TP","SL","TIME","RESULT"]
    rows=[html.Tr([html.Td(t.get("symbol",""),style={"color":TEXT_MAIN,"fontSize":"0.72em","padding":"5px 8px"}),html.Td(t.get("signal",""),style={"color":BULL if "BUY" in str(t.get("signal","")) else BEAR,"fontSize":"0.72em","padding":"5px 8px","fontWeight":"600"}),html.Td(str(t.get("size","")),style={"color":NEUTRAL,"fontSize":"0.72em","padding":"5px 8px"}),html.Td(str(t.get("entry","")),style={"color":TEXT_DIM,"fontSize":"0.72em","padding":"5px 8px"}),html.Td(str(t.get("tp","")),style={"color":BULL,"fontSize":"0.72em","padding":"5px 8px"}),html.Td(str(t.get("sl","")),style={"color":BEAR,"fontSize":"0.72em","padding":"5px 8px"}),html.Td(f"{t.get('in','')} → {t.get('out','')}",style={"color":TEXT_MUTED,"fontSize":"0.65em","padding":"5px 8px"}),html.Td(t.get("result",""),style={"color":BULL if "TP" in str(t.get("result","")) else BEAR if "SL" in str(t.get("result","")) else NEUTRAL,"fontSize":"0.72em","padding":"5px 8px","fontWeight":"600"})],style={"borderBottom":f"1px solid {BORDER}"}) for t in reversed((journal or [])[-20:])]
    return html.Table([html.Thead(html.Tr([html.Th(h,style={"color":TEXT_MUTED,"fontSize":"0.58em","padding":"4px 8px","fontWeight":"500","letterSpacing":"1px","textAlign":"left"}) for h in headers])),html.Tbody(rows)],style={"width":"100%","borderCollapse":"collapse"}),streak_el

@app.callback(Output("chat-open-store","data"),Input("chat-toggle-btn","n_clicks"),Input("chat-close-btn","n_clicks"),State("chat-open-store","data"),prevent_initial_call=True)
def tog_chat(t,c,is_open):
    trig=dash.callback_context.triggered[0]["prop_id"]
    if "close" in trig: return False
    return not is_open

@app.callback(Output("chat-panel","style"),Input("chat-open-store","data"))
def show_chat(is_open):
    base={"width":"380px","backgroundColor":"#0a0912","border":f"1px solid {BORDER}","borderRadius":"14px","overflow":"hidden","boxShadow":"0 8px 40px rgba(0,0,0,0.6)"}
    return {**base,"display":"block" if is_open else "none"}

# ── Chat auto-scroll handled by polling JS in index_string ────────────────────

# ── Phase 1: instant — show user message + typing dots, store pending text ────
@app.callback(
    Output("chat-messages-area","children",allow_duplicate=True),
    Output("chat-pending-store","data"),
    Output("chat-input","value",allow_duplicate=True),
    Input("chat-send-btn","n_clicks"),
    Input("chat-input","n_submit"),
    State("chat-input","value"),
    State("chat-messages-store","data"),
    prevent_initial_call=True,
)
def send_message_phase1(sn, sub, user_text, messages):
    if not user_text or not user_text.strip():
        return dash.no_update, dash.no_update, dash.no_update
    messages = list(messages or [])
    preview = messages + [{"role":"user","content":user_text.strip()}]
    # Show user message immediately + bouncing dots below it
    display = render_chat_messages(preview) + [_typing_bubble()]
    return display, {"text": user_text.strip(), "history": messages}, ""

# ── Phase 2: AI call — triggered by pending store, returns full response ──────
@app.callback(
    Output("chat-messages-store","data"),
    Output("chat-messages-area","children"),
    Output("chat-input","value"),
    Input("chat-pending-store","data"),
    State("session-store","data"),
    State("symbol-input","value"),
    State("interval-dropdown","value"),
    State("signal-text","children"),
    State("rsi-text","children"),
    State("macd-text","children"),
    State("entry-text","children"),
    State("trade-store","data"),
    prevent_initial_call=True,
)
def send_message_phase2(pending, session, symbol, interval, signal, rsi, macd, entry, trade_store):
    if not pending or not pending.get("text"):
        return dash.no_update, dash.no_update, dash.no_update
    user_text = pending["text"]
    messages  = list(pending.get("history") or [])
    plan      = session.get("plan","hustler")
    limits    = PLAN_LIMITS.get(plan, PLAN_LIMITS[None])
    ai_msgs_used = sum(1 for m in messages if m["role"]=="user")
    if ai_msgs_used >= limits["ai_msgs"] and plan not in ["admin","veteran"]:
        messages.append({"role":"user","content":user_text})
        limit_msg = f"⚠️ You've used your {limits['ai_msgs']} daily AI messages. Upgrade to Veteran for unlimited access."
        messages.append({"role":"assistant","content":limit_msg})
        return messages, render_chat_messages(messages), ""
    messages.append({"role":"user","content":user_text})
    ctx_parts = []
    if symbol: ctx_parts.append(f"Symbol: {symbol}")
    if interval: ctx_parts.append(f"Timeframe: {interval}")
    try:
        if signal: ctx_parts.append(f"Current signal: {str(signal)}")
    except: pass
    try:
        if rsi: ctx_parts.append(f"RSI: {str(rsi)}")
    except: pass
    try:
        if macd: ctx_parts.append(f"MACD: {str(macd)}")
    except: pass
    try:
        if entry: ctx_parts.append(f"Entry price: {str(entry)}")
    except: pass
    if trade_store and trade_store.get("in_trade"):
        ctx_parts.append(
            f"User is IN an active {trade_store.get('signal','?')} trade on "
            f"{trade_store.get('symbol','?')} from entry {trade_store.get('entry','?')}, "
            f"TP {trade_store.get('tp','?')}, SL {trade_store.get('sl','?')}"
        )
    context = "\n".join(ctx_parts) if ctx_parts else ""
    ai_reply = call_bojket([{"role":m["role"],"content":m["content"]} for m in messages[-10:]], context=context)
    messages.append({"role":"assistant","content":ai_reply})
    return messages, render_chat_messages(messages), ""


# ── QUICK CHIP CALLBACK (Phase 1 — show user bubble + typing dots) ────────────
@app.callback(
    Output("chat-messages-area","children",allow_duplicate=True),
    Output("chat-pending-store","data",allow_duplicate=True),
    Output("chat-messages-store","data",allow_duplicate=True),
    Input({"type":"quick-chip","index":ALL},"n_clicks"),
    Input("tutorial-replay-btn","n_clicks"),
    State("chat-messages-store","data"),
    prevent_initial_call=True
)
def handle_quick_chip(chip_clicks, replay_clicks, messages):
    trig = ctx.triggered_id
    if not trig: return dash.no_update, dash.no_update, dash.no_update

    # Tutorial replay — clear chat and reset to intro
    if trig == "tutorial-replay-btn":
        return render_chat_messages([]), None, []

    # Quick chip clicked — Phase 1: show user bubble + typing dots immediately
    if isinstance(trig, dict) and trig.get("type") == "quick-chip":
        user_text = trig["index"]
        messages = list(messages or [])
        preview = messages + [{"role": "user", "content": user_text}]
        display = render_chat_messages(preview) + [_typing_bubble()]
        return display, {"text": user_text, "history": messages}, dash.no_update

    return dash.no_update, dash.no_update, dash.no_update


# ── AI LAB CALLBACKS ──────────────────────────────────────────────────────────

@app.callback(
    Output("ailab-panel","style"),
    Output("ailab-open-store","data"),
    Input("ailab-btn","n_clicks"),
    Input("ailab-close-btn","n_clicks"),
    State("ailab-open-store","data"),
    prevent_initial_call=True
)
def toggle_ailab(open_clicks, close_clicks, is_open):
    trig = dash.callback_context.triggered[0]["prop_id"]
    if "ailab-close-btn" in trig:
        return AILAB_PANEL_HIDDEN, False
    if "ailab-btn" in trig and is_open:
        return AILAB_PANEL_HIDDEN, False
    return AILAB_PANEL_SHOWN, True


# ── ADMIN PANEL TOGGLE ────────────────────────────────────────────────────────
@app.callback(
    Output("admin-panel","style"),
    Input("admin-btn","n_clicks"),
    Input("admin-close-btn","n_clicks"),
    State("admin-panel","style"),
    prevent_initial_call=True,
)
def toggle_admin(o, c, style):
    trig = dash.callback_context.triggered[0]["prop_id"]
    is_open = style.get("display") != "none"
    if "admin-close-btn" in trig or ("admin-btn" in trig and is_open):
        return ADMIN_PANEL_HIDDEN
    return ADMIN_PANEL_SHOWN

# ── ADMIN TAB SWITCHER ────────────────────────────────────────────────────────
@app.callback(
    Output("admin-tab-store","data"),
    Input("admin-tab-members-btn","n_clicks"),
    Input("admin-tab-analytics-btn","n_clicks"),
    prevent_initial_call=True,
)
def switch_admin_tab(m, a):
    trig = dash.callback_context.triggered[0]["prop_id"]
    return "analytics" if "analytics" in trig else "members"

# ── ADMIN PANEL CONTENT ───────────────────────────────────────────────────────
@app.callback(
    Output("admin-panel-content","children"),
    Input("admin-panel","style"),
    Input("admin-tab-store","data"),
    prevent_initial_call=True,
)
def render_admin(style, tab):
    if style.get("display") == "none":
        return dash.no_update
    if tab == "analytics":
        return build_admin_analytics()
    return build_admin_content()


@app.callback(
    Output("ailab-content","children"),
    Input("ml-poll-interval","n_intervals"),
    Input("ailab-open-store","data"),
    State("bt-symbol-store","data"),
    State("bt-interval-store","data"),
    State("ml-train-symbols-store","data"),
    State("ml-train-interval-store","data"),
)
def update_ailab(n, is_open, bt_sym, bt_int, train_syms, train_int):
    if not is_open:
        return dash.no_update

    with _ML_LOCK:   ml_state  = dict(_ML_STATE)
    with _BT_LOCK:   bt_state  = dict(_BT_STATE)

    ml_status  = ml_state["status"]
    ml_acc     = ml_state.get("accuracy")
    ml_samples = ml_state.get("n_samples", 0)
    ml_msg     = ml_state.get("message", "")
    ml_err     = ml_state.get("error")
    ml_fi      = ml_state.get("feat_imp")
    ml_prog    = ml_state.get("progress", 0)

    # ── GAME: AI BRAIN SECTION ─────────────────────────────────────────────
    if ml_status == "done":
        brain_color  = BULL
        brain_emoji  = "🏆"
        brain_title  = "AI BRAIN — UNLOCKED"
        brain_sub    = f"Your AI studied {ml_samples:,} real trades and is now boosting every signal."
        brain_stat   = f"Accuracy  {ml_acc}%" if ml_acc else "Active & boosting signals"
        xp_pct       = min(int(ml_acc or 70), 100)
        xp_label     = f"POWER  {xp_pct}%"
    elif ml_status == "training":
        brain_color  = PURPLE_LIGHT
        brain_emoji  = "⚡"
        brain_title  = "AI BRAIN — TRAINING…"
        brain_sub    = ml_msg or "Downloading market data and learning patterns…"
        brain_stat   = f"{ml_prog}% complete"
        xp_pct       = ml_prog
        xp_label     = f"TRAINING  {ml_prog}%"
    elif ml_status == "error":
        brain_color  = BEAR
        brain_emoji  = "✗"
        brain_title  = "TRAINING FAILED"
        brain_sub    = ml_err or "Something went wrong. Try retraining."
        brain_stat   = ""
        xp_pct       = 0
        xp_label     = ""
    else:
        brain_color  = TEXT_MUTED
        brain_emoji  = "💤"
        brain_title  = "AI BRAIN — AWAKENING…"
        brain_sub    = "Bojket is quietly training your AI in the background. It'll be ready soon."
        brain_stat   = "Initialising…"
        xp_pct       = 5
        xp_label     = "STARTING UP"

    train_btn_disabled = (ml_status == "training") or (not HAS_SKLEARN)

    # XP bar
    xp_bar = html.Div([
        html.Div([
            html.Span(xp_label, style={"color":brain_color,"fontSize":"0.6em","fontWeight":"700","letterSpacing":"1px"}),
        ],style={"marginBottom":"4px"}),
        html.Div(
            html.Div(style={"width":f"{xp_pct}%","height":"100%",
                            "background":f"linear-gradient(90deg,{brain_color},{brain_color}aa)",
                            "borderRadius":"4px","transition":"width 0.6s ease"}),
            style={"backgroundColor":f"{brain_color}18","borderRadius":"4px","height":"8px","overflow":"hidden"}
        ),
    ],style={"marginBottom":"12px"})

    # Stats row (only when trained)
    stats_row = html.Div([
        html.Div([html.Div("ACCURACY",style={"color":TEXT_MUTED,"fontSize":"0.55em","letterSpacing":"1px","marginBottom":"2px"}),
                  html.Div(f"{ml_acc}%",style={"color":BULL,"fontWeight":"800","fontSize":"1.1em"})],
                 style={"flex":"1","textAlign":"center","backgroundColor":f"{BULL}08","borderRadius":"8px","padding":"8px 4px"}),
        html.Div([html.Div("TRADES",style={"color":TEXT_MUTED,"fontSize":"0.55em","letterSpacing":"1px","marginBottom":"2px"}),
                  html.Div(f"{ml_samples:,}",style={"color":TEXT_MAIN,"fontWeight":"800","fontSize":"1.1em"})],
                 style={"flex":"1","textAlign":"center","backgroundColor":f"{PURPLE}08","borderRadius":"8px","padding":"8px 4px"}),
        html.Div([html.Div("STATUS",style={"color":TEXT_MUTED,"fontSize":"0.55em","letterSpacing":"1px","marginBottom":"2px"}),
                  html.Div("ACTIVE",style={"color":BULL,"fontWeight":"800","fontSize":"1.1em"})],
                 style={"flex":"1","textAlign":"center","backgroundColor":f"{BULL}08","borderRadius":"8px","padding":"8px 4px"}),
    ],style={"display":"flex","gap":"6px","marginBottom":"12px"}) if (ml_status=="done" and ml_acc) else html.Div()

    ml_section = html.Div([
        # Game header
        html.Div([
            html.Span(brain_emoji, style={"fontSize":"1.6em","marginRight":"10px"}),
            html.Div([
                html.Div(brain_title, style={"color":brain_color,"fontWeight":"900","fontSize":"0.82em","letterSpacing":"1px"}),
                html.Div(brain_sub,  style={"color":TEXT_DIM,"fontSize":"0.72em","marginTop":"2px","lineHeight":"1.4"}),
            ]),
        ],style={"display":"flex","alignItems":"flex-start","marginBottom":"12px",
                 "backgroundColor":f"{brain_color}08","border":f"1px solid {brain_color}25",
                 "borderRadius":"12px","padding":"14px"}),

        xp_bar,
        stats_row,

        # Feature importance (when trained)
        *([html.Div([
            html.Div("TOP SIGNALS YOUR AI LEARNED",style={"color":TEXT_MUTED,"fontSize":"0.58em","letterSpacing":"1px","fontWeight":"700","marginBottom":"8px"}),
            render_feat_importance(ml_fi),
        ],style={"marginBottom":"14px"})] if ml_fi and ml_status=="done" else []),

        # Retrain button
        html.Button(
            "⚡  Retraining…" if ml_status=="training" else "🔄  Retrain AI Brain",
            id="ml-train-btn", n_clicks=0, disabled=train_btn_disabled,
            style={"background":f"linear-gradient(135deg,{PURPLE}30,{PURPLE}15)" if not train_btn_disabled else "transparent",
                   "border":f"1px solid {PURPLE}{'60' if not train_btn_disabled else '25'}",
                   "color":PURPLE_LIGHT if not train_btn_disabled else TEXT_MUTED,
                   "padding":"10px 18px","borderRadius":"8px","fontSize":"0.78em",
                   "cursor":"pointer" if not train_btn_disabled else "default",
                   "fontWeight":"700","width":"100%","marginBottom":"5px",
                   "opacity":"1.0" if not train_btn_disabled else "0.4"}),
        html.Div("Trains on BTC · ETH · SOL · Nasdaq · Gold · EUR/USD  ·  1h candles",
            style={"color":TEXT_MUTED,"fontSize":"0.6em","textAlign":"center","marginBottom":"18px","fontStyle":"italic"}),

        html.Div(style={"height":"1px","backgroundColor":BORDER,"margin":"0 0 18px 0"}),
    ])

    # ── BACKTEST SECTION ───────────────────────────────────────────────────
    bt_status  = bt_state["status"]
    bt_msg     = bt_state.get("message","")
    bt_results = bt_state.get("results")
    bt_prog    = bt_state.get("progress",0)

    bt_sym_opts_top = ["BTC-USD","ETH-USD","SOL-USD","EURUSD=X","NQ=F","GC=F","AAPL","TSLA","CL=F"]
    bt_sym_sel = html.Div([
        html.Span(s, id={"type":"bt-sym-pill","index":s}, n_clicks=0,
            style={"cursor":"pointer","display":"inline-block","fontSize":"0.65em",
                   "padding":"3px 10px","margin":"3px 3px 3px 0","borderRadius":"20px",
                   "border":f"1px solid {BULL if s==bt_sym else BORDER}",
                   "color":BULL if s==bt_sym else TEXT_MUTED,
                   "backgroundColor":f"{BULL}12" if s==bt_sym else "transparent"})
        for s in bt_sym_opts_top
    ], style={"lineHeight":"2.4","marginBottom":"10px"})

    bt_int_opts = [("1 Hour","1h"),("4 Hours","4h"),("Daily","1d")]
    bt_int_btns = html.Div([
        html.Button(l, id={"type":"bt-int-btn","index":v}, n_clicks=0,
            style={"fontSize":"0.65em","padding":"5px 12px","marginRight":"5px","borderRadius":"6px",
                   "cursor":"pointer","border":f"1px solid {BULL if v==bt_int else BORDER}",
                   "color":BULL if v==bt_int else TEXT_MUTED,
                   "backgroundColor":f"{BULL}12" if v==bt_int else "transparent"})
        for l,v in bt_int_opts
    ], style={"marginBottom":"12px"})

    bt_btn_disabled = (bt_status == "running")

    bt_section = html.Div([
        html.Div([
            html.Span("📊",style={"fontSize":"1.3em","marginRight":"10px"}),
            html.Div([
                html.Div("STRATEGY REPLAY",style={"color":TEXT_MAIN,"fontWeight":"900","fontSize":"0.82em","letterSpacing":"1px"}),
                html.Div("Replay Bojket's signals on 2 years of real history. See the win rate before risking real money.",
                         style={"color":TEXT_DIM,"fontSize":"0.72em","marginTop":"2px","lineHeight":"1.4"}),
            ]),
        ],style={"display":"flex","alignItems":"flex-start","marginBottom":"14px",
                 "backgroundColor":f"{BULL}06","border":f"1px solid {BULL}20",
                 "borderRadius":"12px","padding":"14px"}),

        html.Div("Choose asset:",style={"color":TEXT_MUTED,"fontSize":"0.62em","marginBottom":"6px","fontWeight":"600","letterSpacing":"0.5px"}),
        bt_sym_sel,
        html.Div("Timeframe:",style={"color":TEXT_MUTED,"fontSize":"0.62em","marginBottom":"6px","fontWeight":"600","letterSpacing":"0.5px"}),
        bt_int_btns,
        html.Button(
            "◌  Running replay…" if bt_status=="running" else "▶  Run Strategy Replay",
            id="bt-run-btn", n_clicks=0, disabled=bt_btn_disabled,
            style={"background":f"linear-gradient(135deg,{BULL}25,{BULL}10)" if not bt_btn_disabled else "transparent",
                   "border":f"1px solid {BULL}{'50' if not bt_btn_disabled else '20'}","color":BULL,
                   "padding":"10px 18px","borderRadius":"8px","fontSize":"0.78em",
                   "cursor":"pointer" if not bt_btn_disabled else "default",
                   "fontWeight":"700","width":"100%","marginBottom":"10px",
                   "opacity":"1.0" if not bt_btn_disabled else "0.5"}),
        *([_prog_bar(bt_prog, BULL)] if bt_status=="running" else []),
        html.Div(bt_msg,style={"color":TEXT_MUTED if bt_status!="error" else BEAR,"fontSize":"0.68em","marginBottom":"8px","fontStyle":"italic"}),
        render_backtest_results(bt_results),
    ])

    return html.Div([ml_section, bt_section])


# Toggle ML training symbols
@app.callback(
    Output("ml-train-symbols-store","data"),
    Input({"type":"ml-sym-pill","index":ALL},"n_clicks"),
    State("ml-train-symbols-store","data"),
    prevent_initial_call=True
)
def toggle_ml_sym(_, syms):
    tid = ctx.triggered_id
    if not tid: return syms
    name = tid["index"]
    syms = list(syms or [])
    if name in syms: syms.remove(name)
    elif len(syms) < 10: syms.append(name)
    return syms

# Toggle ML training interval
@app.callback(
    Output("ml-train-interval-store","data"),
    Input({"type":"ml-int-btn","index":ALL},"n_clicks"),
    prevent_initial_call=True
)
def toggle_ml_int(_):
    tid = ctx.triggered_id
    return tid["index"] if tid else "1h"

# Toggle backtest symbol
@app.callback(
    Output("bt-symbol-store","data"),
    Input({"type":"bt-sym-pill","index":ALL},"n_clicks"),
    prevent_initial_call=True
)
def toggle_bt_sym(_):
    tid = ctx.triggered_id
    return tid["index"] if tid else "BTC-USD"

# Toggle backtest interval
@app.callback(
    Output("bt-interval-store","data"),
    Input({"type":"bt-int-btn","index":ALL},"n_clicks"),
    prevent_initial_call=True
)
def toggle_bt_int(_):
    tid = ctx.triggered_id
    return tid["index"] if tid else "1h"

# Start ML training
@app.callback(
    Output("ml-train-btn","n_clicks"),
    Input("ml-train-btn","n_clicks"),
    State("ml-train-symbols-store","data"),
    State("ml-train-interval-store","data"),
    prevent_initial_call=True
)
def start_training_cb(n, syms, interval):
    if n and n > 0:
        start_ml_training(symbols=syms or ["BTC-USD","ETH-USD","SOL-USD","NQ=F","GC=F","EURUSD=X"],
                          interval=interval or "1h")
    return 0

# Start backtest
@app.callback(
    Output("bt-run-btn","n_clicks"),
    Input("bt-run-btn","n_clicks"),
    State("bt-symbol-store","data"),
    State("bt-interval-store","data"),
    prevent_initial_call=True
)
def start_backtest_cb(n, symbol, interval):
    if n and n > 0:
        start_backtest(symbol=symbol or "BTC-USD", interval=interval or "1h")
    return 0


# ── MAIN CHART + SIGNAL UPDATE CALLBACK ──────────────────────────────────────

@app.callback(
    Output("candle-chart","figure"),
    Output("signal-text","children"),Output("signal-text","style"),
    Output("confidence-div","children"),Output("ml-score-div","children"),
    Output("signal-sub","children"),
    Output("trend-text","children"),Output("trend-text","style"),
    Output("rsi-text","children"),Output("rsi-text","style"),Output("rsi-hint","children"),
    Output("macd-text","children"),Output("macd-hint","children"),Output("macd-hint","style"),
    Output("entry-text","children"),Output("tp-text","children"),Output("sl-text","children"),
    Output("position-size-display","children"),Output("tp-pnl-preview","children"),Output("sl-pnl-preview","children"),
    Output("trade-status","children"),Output("trade-status-hint","children"),
    Output("trade-panel","style"),Output("buy-btn-div","children"),
    Output("market-summary","children"),Output("breakdown-content","children"),
    Output("patterns-div","children"),Output("tips-div","children"),
    Output("pattern-history-div","children"),Output("pattern-history-store","data"),
    Output("forecast-div","children"),
    Output("alert-triggered-bar","style"),Output("last-updated","children"),
    Input("auto-refresh","n_intervals"),Input("refresh-btn","n_clicks"),
    Input("symbol-input","value"),Input("interval-dropdown","value"),
    Input("trade-store","data"),Input("active-patterns-store","data"),
    Input("chart-theme","data"),Input("bb-store","data"),Input("pd-store","data"),
    State("alert-store","data"),State("pattern-history-store","data"),State("session-store","data"),
)
def update(n,clicks,symbol,interval,trade_store,active_patterns,theme,show_bb,show_pd,alert_store,pat_history,session):
    if not symbol: symbol="BTC-USD"
    plan=session.get("plan","hustler")
    period_map={"1m":"5d","5m":"5d","15m":"1mo","30m":"1mo","1h":"3mo","2h":"6mo","3h":"6mo","4h":"6mo","1d":"2y"}
    df=fetch_data(symbol.upper().strip(),interval=interval,period=period_map.get(interval,"5d"))
    is_dark=theme!="light"; bg_c="#080808" if is_dark else "#f8f8fc"; bg_p="#080808" if is_dark else "#ffffff"
    grid_c="rgba(255,255,255,0.025)" if is_dark else "rgba(0,0,0,0.05)"; tick_c="#2a2040" if is_dark else "#bbb"
    bull_c=BULL if is_dark else "#059669"; bear_c=BEAR if is_dark else "#dc2626"
    hov_bg="#0d0d0d" if is_dark else "#fff"; hov_fc=TEXT_MAIN if is_dark else "#111"
    no={"display":"none"}; alert_bar_off={"display":"none"}

    if df is None or df.empty:
        fig=go.Figure(); fig.update_layout(paper_bgcolor=bg_p,plot_bgcolor=bg_c,font_color=TEXT_MUTED,title=f"No data — {symbol}")
        empty=html.Div("No data.",style={"color":TEXT_MUTED,"fontSize":"0.78em","fontStyle":"italic"})
        return (fig,"—",{"color":TEXT_MUTED,"fontSize":"2em"},html.Div(),html.Div(),"No data","—",{"color":TEXT_MUTED},"-",{"color":TEXT_MUTED},"","-","",{"color":TEXT_MUTED},"-","-","-","","","","-","-",no,"","Could not load data.",html.Div(),[],[],empty,pat_history,html.Div(),alert_bar_off,"—")

    fig=make_subplots(rows=2,cols=1,shared_xaxes=True,vertical_spacing=0.01,row_heights=[0.78,0.22])
    fig.add_trace(go.Candlestick(x=df.index,open=df['open'],high=df['high'],low=df['low'],close=df['close'],
        increasing=dict(line=dict(color=bull_c, width=1.5), fillcolor=bull_c),
        decreasing=dict(line=dict(color=bear_c, width=1.5), fillcolor=bear_c),
        name=symbol, hoverinfo="x+y",
        whiskerwidth=0,          # no wick tip caps — clean TradingView look
    ), row=1, col=1)
    if len(df)>=50:
        fig.add_trace(go.Scatter(x=df.index,y=df['close'].ewm(span=50,adjust=False).mean(),line=dict(color=MA50_COLOR,width=1.2),name="EMA 50",hoverinfo="skip"),row=1,col=1)
        fig.add_trace(go.Scatter(x=df.index,y=df['close'].ewm(span=20,adjust=False).mean(),line=dict(color=MA20_COLOR,width=1),name="EMA 20",hoverinfo="skip"),row=1,col=1)
    if 'volume' in df.columns:
        tp_=(df['high']+df['low']+df['close'])/3; vol_=df['volume'].replace(0,np.nan).fillna(1)
        fig.add_trace(go.Scatter(x=df.index,y=(tp_*vol_).cumsum()/vol_.cumsum(),line=dict(color="rgba(250,204,21,0.5)",width=1,dash="dot"),name="VWAP",hoverinfo="skip"),row=1,col=1)
    if show_bb:
        _,bb_upper,bb_lower=get_bollinger_bands(df)
        if bb_upper is not None:
            fig.add_trace(go.Scatter(x=df.index,y=bb_upper,line=dict(color="rgba(167,139,250,0.35)",width=1,dash="dot"),name="BB Upper",hoverinfo="skip"),row=1,col=1)
            fig.add_trace(go.Scatter(x=df.index,y=bb_lower,line=dict(color="rgba(167,139,250,0.35)",width=1,dash="dot"),fill="tonexty",fillcolor="rgba(124,58,237,0.04)",name="BB Lower",hoverinfo="skip"),row=1,col=1)
    if show_pd:
        pd_high,pd_low=get_prev_day_levels(df)
        if pd_high: fig.add_hline(y=pd_high,line=dict(color="rgba(250,204,21,0.5)",width=1,dash="dash"),annotation_text="Prev H",annotation_font_color="rgba(250,204,21,0.7)",annotation_font_size=9,row=1,col=1)
        if pd_low:  fig.add_hline(y=pd_low, line=dict(color="rgba(167,139,250,0.5)",width=1,dash="dash"),annotation_text="Prev L",annotation_font_color="rgba(167,139,250,0.7)",annotation_font_size=9,row=1,col=1)
    sup_levels,res_levels=get_support_resistance(df)
    for sv in sup_levels: fig.add_hline(y=sv,line=dict(color="rgba(52,211,153,0.3)",width=1,dash="dot"),annotation_text="S",annotation_font_color="rgba(52,211,153,0.5)",annotation_font_size=8,row=1,col=1)
    for rv in res_levels: fig.add_hline(y=rv,line=dict(color="rgba(248,113,113,0.3)",width=1,dash="dot"),annotation_text="R",annotation_font_color="rgba(248,113,113,0.5)",annotation_font_size=8,row=1,col=1)
    if active_patterns:
        pdata=scan_patterns(df,active_patterns)
        for pname,data in pdata.items():
            if not data["x"]: continue
            s=data["sentiment"]; color=PAT_COLOR.get(s,NEUTRAL)
            abbr=PAT_ABBR.get(pname,pname[:3].upper())
            n_pts=len(data["x"])
            shape="triangle-up" if s=="bullish" else "triangle-down" if s=="bearish" else "diamond"
            tpos="top center" if s=="bullish" else "bottom center"
            fig.add_trace(go.Scatter(
                x=data["x"], y=data["y"],
                mode="markers+text",
                marker=dict(symbol=shape, size=10, color=color,
                            opacity=0.92, line=dict(width=0)),
                text=[abbr]*n_pts,
                textposition=tpos,
                textfont=dict(color=color, size=8, family="Inter,monospace"),
                hovertext=[f"<b>{pname}</b><br><span style='color:#aaa'>{DESCS.get(pname,'')}</span>"
                           for _ in data["x"]],
                hoverinfo="text",
                name=pname, showlegend=True,
            ), row=1, col=1)
    if 'volume' in df.columns:
        vcol=[bull_c if df['close'].iloc[i]>=df['open'].iloc[i] else bear_c for i in range(len(df))]
        fig.add_trace(go.Bar(x=df.index,y=df['volume'],marker_color=vcol,marker_opacity=0.45,name="Vol",hoverinfo="x+y",showlegend=False),row=2,col=1)

    x_min,x_max=df.index.min(),df.index.max()
    y_min,y_max=df['low'].min(),df['high'].max()
    y_range = y_max - y_min if y_max != y_min else 1
    y_pad_chart = y_range * 0.05
    ax=dict(showgrid=True,gridcolor=grid_c,zeroline=False,showline=False,tickfont=dict(color=tick_c,size=9))
    icon=ASSET_ICONS.get(symbol,""); name_label=LABELS.get(symbol,symbol); title_color=TEXT_MAIN if is_dark else "#111"

    # ── Initial view: show the last N candles so bodies are fat by default ──
    # (Like TradingView: zooming in → fatter, zooming out → thinner — auto)
    _view_candles = {"1m":60,"5m":80,"15m":80,"30m":60,"1h":72,"2h":60,"3h":56,"4h":60,"1d":60}
    n_view = _view_candles.get(interval, 80)
    x_view_min = df.index[-min(n_view, len(df))]   # oldest candle in initial window

    # ── Minimum x-range width: 3 candle widths — prevents extreme zoom that
    #    makes Plotly try to render sub-tick datetime labels (spaz territory) ──
    _candle_ms = {"1m":60e3,"5m":300e3,"15m":900e3,"30m":1800e3,
                  "1h":3600e3,"2h":7200e3,"3h":10800e3,"4h":14400e3,"1d":86400e3}
    one_candle_ms = _candle_ms.get(interval, 300e3)
    min_x_range_ms = one_candle_ms * 3   # can't zoom in tighter than 3 candles

    fig.update_layout(
        uirevision=f"{symbol}_{interval}",
        paper_bgcolor=bg_p, plot_bgcolor=bg_c,
        font=dict(color=TEXT_DIM, size=10, family="Inter,sans-serif"),
        xaxis_rangeslider_visible=False,
        title=dict(
            text=f"<b style='color:{title_color}'>{icon}  {name_label}</b><span style='color:{TEXT_MUTED};font-size:10px'>  {interval}</span>",
            font=dict(size=13), x=0.01, y=0.99),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=8, color=TEXT_MUTED),
                    orientation="h", x=0, y=1.025),
        hovermode="x unified",
        hoverlabel=dict(bgcolor=hov_bg, bordercolor=BORDER, font=dict(color=hov_fc, size=10)),
        # ── X axis: initial view = last N candles; soft left wall at oldest data ──
        xaxis=dict(**ax,
            range=[x_view_min, x_max],
            fixedrange=False,
            minallowed=x_min,
        ),
        # ── Y axis: completely free — no snap bounds, silky smooth ──
        yaxis=dict(**ax,
            range=[y_min - y_pad_chart, y_max + y_pad_chart],
            fixedrange=False, side="right"),
        xaxis2=dict(**ax),
        yaxis2=dict(showgrid=False, zeroline=False, showline=False,
                    tickfont=dict(color=tick_c, size=8), side="right"),
        margin=dict(l=0, r=65, t=26, b=28),
        dragmode="pan",
    )

    patterns=detect_patterns(df)
    raw_signal,sig_color,confidence,reasons,ema_trend=superintelligent_signal(df,symbol,interval,patterns,plan)
    rsi,macd,macd_sig,last_price=get_indicators(df)

    in_trade=(trade_store or {}).get("in_trade",False); in_cooldown=(trade_store or {}).get("cooldown",False)
    cons_losses=(trade_store or {}).get("consecutive_losses",0); last_result=(trade_store or {}).get("last_result",""); cooldown_since=(trade_store or {}).get("cooldown_since")
    if in_cooldown and cooldown_since:
        try:
            elapsed=(datetime.now()-datetime.fromisoformat(cooldown_since)).total_seconds(); wait_time=300 if "SL" in str(last_result) else 120; min_conf=85 if cons_losses>=2 else 72
            if elapsed>=wait_time and confidence>=min_conf: in_cooldown=False
        except: pass

    signal="WAIT" if in_cooldown else raw_signal
    entry,tp,sl=get_levels(df,signal,custom_tp=(trade_store or {}).get("custom_tp") if in_trade else None,custom_sl=(trade_store or {}).get("custom_sl") if in_trade else None)
    if in_trade: entry=(trade_store or {}).get("entry",entry); tp=(trade_store or {}).get("tp",tp); sl=(trade_store or {}).get("sl",sl)

    # ── Draw TP / SL lines on chart (active trade only) ──────────────────────
    if in_trade and tp:
        fig.add_hline(y=tp,line=dict(color="rgba(52,211,153,0.75)",width=1.5,dash="dash"),
                      annotation_text="  TP",annotation_font_color="rgba(52,211,153,0.9)",
                      annotation_font_size=9,row=1,col=1)
    if in_trade and sl:
        fig.add_hline(y=sl,line=dict(color="rgba(248,113,113,0.75)",width=1.5,dash="dash"),
                      annotation_text="  SL",annotation_font_color="rgba(248,113,113,0.9)",
                      annotation_font_size=9,row=1,col=1)
    if in_trade and entry:
        fig.add_hline(y=entry,line=dict(color="rgba(167,139,250,0.5)",width=1,dash="dot"),
                      annotation_text="  Entry",annotation_font_color="rgba(167,139,250,0.8)",
                      annotation_font_size=9,row=1,col=1)

    summary=get_summary(signal,ema_trend,rsi,in_cooldown,reasons)
    breakdown_content=render_breakdown(reasons,signal,confidence)

    bar_color=BULL if signal=="BUY" else BEAR if signal=="SELL" else NEUTRAL
    conf_el=html.Div([html.Div([html.Span(f"{confidence}%",style={"color":bar_color,"fontWeight":"700","fontSize":"0.92em"}),html.Span(" engine score",style={"color":TEXT_MUTED,"fontSize":"0.68em","marginLeft":"5px"})],style={"marginBottom":"4px"}),html.Div(html.Div(style={"width":f"{confidence}%","backgroundColor":bar_color,"height":"4px","borderRadius":"4px"}),style={"backgroundColor":"#1e1a2e","borderRadius":"4px","height":"4px"})]) if confidence>0 else html.Div()

    # ML score badge
    bull_prob, bear_prob = ml_predict(df)
    if bull_prob is not None:
        ml_dir = "BULL" if bull_prob > 55 else "BEAR" if bull_prob < 45 else "NEUT"
        ml_col = BULL if bull_prob > 55 else BEAR if bull_prob < 45 else TEXT_MUTED
        ml_val = bull_prob if bull_prob >= 50 else bear_prob
        ml_score_el = html.Div([
            html.Span("🧠 ML ",style={"color":TEXT_MUTED,"fontSize":"0.62em"}),
            html.Span(f"{ml_dir} {ml_val}%",style={"color":ml_col,"fontSize":"0.65em","fontWeight":"700",
                "border":f"1px solid {ml_col}40","backgroundColor":f"{ml_col}10",
                "padding":"1px 7px","borderRadius":"20px"}),
        ],style={"marginTop":"4px"})
    else:
        ml_score_el = html.Div()

    sig_sub=f"{icon}  {name_label}  ·  {round(last_price,4) if last_price else '—'}"
    trend_col=BULL if ema_trend=="bullish" else BEAR if ema_trend=="bearish" else NEUTRAL
    trend_label={"bullish":"↑  Uptrend (EMA)","bearish":"↓  Downtrend (EMA)"}.get(ema_trend,"→  Sideways")
    if rsi: rsi_color=BEAR if rsi>70 else BULL if rsi<30 else TEXT_MAIN; rsi_hint="Overbought" if rsi>70 else "Oversold" if rsi<30 else "Neutral"
    else: rsi_color,rsi_hint=TEXT_MAIN,""
    macd_txt,macd_col="",TEXT_DIM
    if macd is not None and macd_sig is not None:
        if macd>macd_sig: macd_txt,macd_col="▲ Bullish",BULL
        else:             macd_txt,macd_col="▼ Bearish",BEAR

    entry_txt=str(entry) if entry else "—"; tp_txt=str(tp) if tp else "—"; sl_txt=str(sl) if sl else "—"
    trade_style={"display":"block"} if in_trade else {"display":"none"}
    pos_size=(trade_store or {}).get("position_size"); pos_display=f"Size: {pos_size} units" if pos_size else "Position size not set"
    tp_preview=sl_preview=""
    if pos_size and entry and tp and sl:
        try:
            t_sig=(trade_store or {}).get("signal",signal); tp_pnl=calc_pnl(t_sig,entry,tp,pos_size); sl_pnl=calc_pnl(t_sig,entry,sl,pos_size)
            tp_preview=f"+{tp_pnl}" if tp_pnl and tp_pnl>0 else str(tp_pnl); sl_preview=str(sl_pnl) if sl_pnl else ""
        except: pass

    t_status=t_hint="—"
    if in_trade and last_price and tp and sl and entry:
        try:
            t_sig=(trade_store or {}).get("signal",signal); cur=float(last_price); pnl=calc_pnl(t_sig,entry,cur,pos_size) if pos_size else None
            pnl_str=f"{'+' if pnl and pnl>0 else ''}{pnl}" if pnl is not None else ""
            if t_sig=="BUY":
                if cur>=float(tp):   t_status,t_hint="✅  TP Hit!",f"Profit: {pnl_str}"
                elif cur<=float(sl): t_status,t_hint="❌  SL Hit",f"Loss: {pnl_str}"
                elif pnl and pnl>0:  t_status,t_hint=f"▲ {pnl_str}","Looking good ↑"
                else:                t_status,t_hint=f"▼ {pnl_str}","Watch your SL"
            else:
                if cur<=float(tp):   t_status,t_hint="✅  TP Hit!",f"Profit: {pnl_str}"
                elif cur>=float(sl): t_status,t_hint="❌  SL Hit",f"Loss: {pnl_str}"
                elif pnl and pnl>0:  t_status,t_hint=f"▲ {pnl_str}","Looking good ↓"
                else:                t_status,t_hint=f"▼ {pnl_str}","Watch your SL"
        except: t_status,t_hint="Active","Monitoring..."

    if in_cooldown: buy_btn=html.Div([html.Div("⏳  Analyzing next opportunity...",style={"color":NEUTRAL,"fontSize":"0.78em","fontWeight":"600","marginBottom":"3px"}),html.Div("Waiting for full multi-timeframe alignment.",style={"color":TEXT_MUTED,"fontSize":"0.65em","fontStyle":"italic"})])
    elif signal=="BUY" and not in_trade: buy_btn=html.Button("✅  I Bought — Set Trade Details",id="i-bought-btn",n_clicks=0,style={"backgroundColor":"rgba(52,211,153,0.08)","border":"1px solid rgba(52,211,153,0.3)","color":BULL,"padding":"5px 14px","borderRadius":"6px","fontSize":"0.73em","cursor":"pointer","width":"100%"})
    elif signal=="SELL" and not in_trade: buy_btn=html.Button("✅  I Sold — Set Trade Details",id="i-bought-btn",n_clicks=0,style={"backgroundColor":"rgba(248,113,113,0.08)","border":"1px solid rgba(248,113,113,0.3)","color":BEAR,"padding":"5px 14px","borderRadius":"6px","fontSize":"0.73em","cursor":"pointer","width":"100%"})
    elif in_trade: buy_btn=html.Span("● Trade Active",style={"color":BULL,"fontSize":"0.7em","fontWeight":"500"})
    else: buy_btn=""

    display_signal="..." if in_cooldown else signal
    display_color=NEUTRAL if in_cooldown else sig_color; sig_font_size="2em" if in_cooldown else "3.2em"

    pattern_badges=[html.Span([html.Span(SEN_EMOJI.get(s,""),style={"marginRight":"5px","fontSize":"0.82em"}),html.Span(name,style={"fontWeight":"500","color":TEXT_MAIN})],style={"display":"inline-block","margin":"2px 4px 2px 0","padding":"3px 11px","borderRadius":"20px","fontSize":"0.73em","backgroundColor":f"{PAT_COLOR.get(s,NEUTRAL)}15","border":f"1px solid {PAT_COLOR.get(s,NEUTRAL)}50","color":PAT_COLOR.get(s,NEUTRAL)}) for name,s,_ in patterns] or [html.Div("No strong patterns on this candle.",style={"color":TEXT_DIM,"fontSize":"0.78em","fontStyle":"italic"})]

    tips_list=[]
    for name,s,desc in patterns:
        color=PAT_COLOR.get(s,NEUTRAL)
        tips_list.append(html.Div([html.Div([html.Span(SEN_EMOJI.get(s,""),style={"fontSize":"1.05em","marginRight":"8px"}),html.Span(name,style={"fontWeight":"600","color":color,"fontSize":"0.86em","marginRight":"7px"}),html.Span(SEN_LABEL.get(s,""),style={"fontSize":"0.62em","color":color,"opacity":"0.7","fontStyle":"italic"})],style={"marginBottom":"3px"}),html.Div(desc,style={"fontSize":"0.76em","color":TEXT_DIM,"paddingLeft":"2px","lineHeight":"1.5"})],style={"backgroundColor":f"{color}07","border":f"1px solid {color}25","borderRadius":"7px","padding":"8px 12px","marginBottom":"5px"}))
    if rsi and rsi>70: tips_list.append(html.Div([html.Div([html.Span("⚠️",style={"marginRight":"8px"}),html.Span("Overbought",style={"fontWeight":"600","color":"#facc15","fontSize":"0.86em","marginRight":"7px"}),html.Span("RSI > 70",style={"fontSize":"0.62em","color":"#facc15","opacity":"0.7","fontStyle":"italic"})]),html.Div("Price is extended — elevated risk for buyers.",style={"fontSize":"0.76em","color":TEXT_DIM})],style={"backgroundColor":"rgba(250,204,21,0.04)","border":"1px solid rgba(250,204,21,0.15)","borderRadius":"7px","padding":"8px 12px","marginBottom":"5px"}))
    if rsi and rsi<30: tips_list.append(html.Div([html.Div([html.Span("💡",style={"marginRight":"8px"}),html.Span("Oversold",style={"fontWeight":"600","color":BULL,"fontSize":"0.86em","marginRight":"7px"}),html.Span("RSI < 30",style={"fontSize":"0.62em","color":BULL,"opacity":"0.7","fontStyle":"italic"})]),html.Div("Price has dropped hard — watch for a potential bounce.",style={"fontSize":"0.76em","color":TEXT_DIM})],style={"backgroundColor":"rgba(52,211,153,0.04)","border":"1px solid rgba(52,211,153,0.15)","borderRadius":"7px","padding":"8px 12px","marginBottom":"5px"}))
    if not tips_list: tips_list=[html.Div("Market is calm — no tips right now.",style={"color":TEXT_DIM,"fontSize":"0.78em","fontStyle":"italic"})]

    now_str=datetime.now().strftime("%H:%M"); new_history=list(pat_history or [])
    for name,s,_ in patterns:
        entry_h={"name":name,"sentiment":s,"time":now_str,"symbol":f"{icon} {name_label}"}
        if not new_history or new_history[-1].get("name")!=name or new_history[-1].get("symbol")!=entry_h["symbol"]: new_history.append(entry_h)
    new_history=new_history[-10:]
    hist_el=html.Div([html.Div([html.Span(SEN_EMOJI.get(h.get("sentiment","neutral"),""),style={"marginRight":"6px"}),html.Span(h.get("name",""),style={"color":PAT_COLOR.get(h.get("sentiment","neutral"),NEUTRAL),"fontWeight":"500","fontSize":"0.78em","marginRight":"8px"}),html.Span(h.get("symbol",""),style={"color":TEXT_MUTED,"fontSize":"0.68em","marginRight":"8px"}),html.Span(h.get("time",""),style={"color":TEXT_MUTED,"fontSize":"0.65em"})],style={"padding":"4px 0","borderBottom":f"1px solid {BORDER}"}) for h in reversed(new_history)]) if new_history else html.Div("No patterns detected yet.",style={"color":TEXT_DIM,"fontSize":"0.78em","fontStyle":"italic"})

    alert_triggered=alert_bar_off
    if alert_store and alert_store.get("active") and last_price and alert_store.get("price"):
        if abs(float(last_price)-float(alert_store["price"]))/max(float(alert_store["price"]),0.0001)<0.002: alert_triggered={"display":"block"}

    # ── Short-term forecast ───────────────────────────────────────────────────
    forecast     = compute_short_term_forecast(df, interval)
    forecast_el  = render_forecast_card(forecast)

    now=datetime.now().strftime("%H:%M:%S")
    return (fig,display_signal,{"color":display_color,"fontSize":sig_font_size,"fontWeight":"700","letterSpacing":"-2px","lineHeight":"1"},conf_el,ml_score_el,sig_sub,trend_label,{"color":trend_col,"fontWeight":"600","fontSize":"1.05em"},str(rsi) if rsi else "—",{"color":rsi_color,"fontWeight":"600"},rsi_hint,str(macd) if macd else "—",macd_txt,{"color":macd_col},entry_txt,tp_txt,sl_txt,pos_display,tp_preview,sl_preview,t_status,t_hint,trade_style,buy_btn,summary,breakdown_content,pattern_badges,tips_list,hist_el,new_history,forecast_el,alert_triggered,f"Updated  {now}")

# ── Show the Bojket loader whenever route changes to /dashboard ──────────────
app.clientside_callback(
    """
    function(pathname) {
        var loader = document.getElementById('bojket-loader');
        if (!loader) return '';
        if (pathname === '/dashboard') {
            loader.style.display = 'flex';
            loader.style.opacity = '1';
            // Hide once the chart canvas is ready, or after 8s as a hard cap
            var tries = 0;
            function check() {
                tries++;
                var chart = document.getElementById('live-chart');
                var svg = chart && chart.querySelector('.main-svg');
                if (svg || tries > 55) {
                    loader.style.opacity = '0';
                    setTimeout(function(){ loader.style.display = 'none'; }, 500);
                } else {
                    setTimeout(check, 150);
                }
            }
            setTimeout(check, 100);
        }
        return '';
    }
    """,
    Output("zoom-guard-sink", "children", allow_duplicate=True),
    Input("url", "pathname"),
    prevent_initial_call=True,
)
if __name__ == "__main__":
    app.run(debug=True)
