# ══════════════════════════════════════════════════════════════════════════════
#  trading_styles.py  —  Trading style presets that tune the signal engine
# ══════════════════════════════════════════════════════════════════════════════

TRADING_STYLES = {
    "scalper": {
        "key": "scalper",
        "name": "Scalper",
        "emoji": "⚡",
        "tagline": "Seconds-to-minutes • Many small wins",
        "description": "You enter and exit in seconds or minutes. The signal will use extreme RSI thresholds (25/75), tight TP:SL ratios (1:1), and prioritize 1m–5m timeframes. Best for high-volatility periods with tight spreads. Many small wins, low hold time.",
        "rsi_low": 25,
        "rsi_high": 75,
        "tp_mult": 1.0,
        "sl_mult": 1.0,
        "min_score": 55,   # easier signal trigger (more frequent)
        "preferred_tfs": ["1m", "5m"],
    },
    "day_trader": {
        "key": "day_trader",
        "name": "Day Trader",
        "emoji": "📊",
        "tagline": "Minutes-to-hours • Balanced approach",
        "description": "Open and close trades within the same day. Standard RSI thresholds (30/70), 1.5:1 to 2:1 reward-to-risk, focused on 5m–1h timeframes. Most common style — balanced frequency and reward. The default for new traders.",
        "rsi_low": 30,
        "rsi_high": 70,
        "tp_mult": 1.5,
        "sl_mult": 1.0,
        "min_score": 62,   # default
        "preferred_tfs": ["5m", "15m", "30m", "1h"],
    },
    "swing_trader": {
        "key": "swing_trader",
        "name": "Swing Trader",
        "emoji": "🌊",
        "tagline": "Hours-to-days • Catch the bigger moves",
        "description": "Hold trades for hours or days, riding multi-day swings. Loose RSI thresholds (35/65), wide 2:1 to 3:1 reward-to-risk, focused on 1h–4h timeframes. Fewer signals, but each one has bigger profit potential. Requires patience.",
        "rsi_low": 35,
        "rsi_high": 65,
        "tp_mult": 2.5,
        "sl_mult": 1.2,
        "min_score": 70,   # stricter (fewer but stronger signals)
        "preferred_tfs": ["1h", "2h", "4h"],
    },
    "position_trader": {
        "key": "position_trader",
        "name": "Position Trader",
        "emoji": "🏛️",
        "tagline": "Days-to-weeks • Macro-driven moves",
        "description": "Hold positions for days or weeks, trading on macro trends. Loosest RSI thresholds (40/60), large 3:1 to 5:1 reward-to-risk, focused on 4h–1d timeframes. Few but high-conviction trades. Requires strong fundamentals view.",
        "rsi_low": 40,
        "rsi_high": 60,
        "tp_mult": 4.0,
        "sl_mult": 1.5,
        "min_score": 75,   # strictest
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