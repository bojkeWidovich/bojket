# ══════════════════════════════════════════════════════════════════════════════
#  trading_styles.py  —  Trading style presets that tune the signal engine
# ══════════════════════════════════════════════════════════════════════════════

TRADING_STYLES = {
    "scalper": {
        "key": "scalper",
        "name": "SCALPER",
        "emoji": "⚡",
        "tagline": "Seconds to minutes • Many small wins",
        "description": "Quick in, quick out. Signal uses extreme RSI (25/75), tight 1:1 risk-reward, focused on 1m–5m. Triggers more often. Best in high volatility.",
        "rsi_low": 25,
        "rsi_high": 75,
        "tp_mult": 1.0,
        "sl_mult": 1.0,
        "min_score": 55,
        "preferred_tfs": ["1m", "5m"],
    },
    "day_trader": {
        "key": "day_trader",
        "name": "DAY TRADER",
        "emoji": "📊",
        "tagline": "Minutes to hours • Balanced approach",
        "description": "Open and close within the day. Standard RSI (30/70), 1.5:1 reward-to-risk, focused on 5m–1h. Most common style. Default for new traders.",
        "rsi_low": 30,
        "rsi_high": 70,
        "tp_mult": 1.5,
        "sl_mult": 1.0,
        "min_score": 62,
        "preferred_tfs": ["5m", "15m", "30m", "1h"],
    },
    "swing_trader": {
        "key": "swing_trader",
        "name": "SWING TRADER",
        "emoji": "🌊",
        "tagline": "Hours to days • Catch bigger moves",
        "description": "Hold for hours or days. Loose RSI (35/65), wide 2.5:1 risk-reward, focused on 1h–4h. Fewer signals, bigger profit targets. Requires patience.",
        "rsi_low": 35,
        "rsi_high": 65,
        "tp_mult": 2.5,
        "sl_mult": 1.2,
        "min_score": 70,
        "preferred_tfs": ["1h", "2h", "4h"],
    },
    "position_trader": {
        "key": "position_trader",
        "name": "POSITION TRADER",
        "emoji": "🏛️",
        "tagline": "Days to weeks • Macro moves",
        "description": "Hold for days or weeks. Loosest RSI (40/60), 4:1 risk-reward, focused on 4h–1d. Few but high-conviction trades. Macro view required.",
        "rsi_low": 40,
        "rsi_high": 60,
        "tp_mult": 4.0,
        "sl_mult": 1.5,
        "min_score": 75,
        "preferred_tfs": ["4h", "1d"],
    },
}


def get_style(key):
    """Return style dict by key, defaulting to day_trader."""
    return TRADING_STYLES.get(key or "day_trader", TRADING_STYLES["day_trader"])


def style_context_for_ai(key):
    """Return a string describing the user's style for the Bojket AI's system prompt."""
    s = get_style(key)
    return (
        f"User's trading style: {s['name']} ({s['emoji']}). "
        f"{s['tagline']}. "
        f"When giving advice, frame it for a {s['name']} — reference their typical "
        f"hold time, preferred timeframes ({', '.join(s['preferred_tfs'])}), and the "
        f"reward-to-risk profile that fits their style."
    )