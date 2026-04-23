# ══════════════════════════════════════════════════════════════════════════════
#  ranks.py  —  Capybara ranking system
# ══════════════════════════════════════════════════════════════════════════════

from datetime import datetime, timedelta
from dash import html

# ── Rank definitions (order matters: low → high) ─────────────────────────────
RANKS = [
    {
        "key": "bronze",
        "name": "Capybara Rookie",
        "tier": "BRONZE",
        "min_trades": 0,
        "min_winrate": 0.0,
        "needs_active": False,
        # brown gradient
        "gradient": "linear-gradient(135deg, #8B4513 0%, #CD7F32 50%, #A0522D 100%)",
        "glow": "rgba(205,127,50,0.55)",
        "text": "#FFE8CC",
        "border": "#CD7F32",
    },
    {
        "key": "silver",
        "name": "Capybara Intermediate",
        "tier": "SILVER",
        "min_trades": 5,
        "min_winrate": 0.40,
        "needs_active": False,
        # silver gradient
        "gradient": "linear-gradient(135deg, #707070 0%, #C0C0C0 50%, #8E8E8E 100%)",
        "glow": "rgba(192,192,192,0.55)",
        "text": "#FFFFFF",
        "border": "#C0C0C0",
    },
    {
        "key": "gold",
        "name": "Capybara Hustler",
        "tier": "GOLD",
        "min_trades": 15,
        "min_winrate": 0.50,
        "needs_active": False,
        # gold gradient
        "gradient": "linear-gradient(135deg, #B8860B 0%, #FFD700 50%, #DAA520 100%)",
        "glow": "rgba(255,215,0,0.60)",
        "text": "#3B2500",
        "border": "#FFD700",
    },
    {
        "key": "platinum",
        "name": "Capybara Master",
        "tier": "PLATINUM",
        "min_trades": 40,
        "min_winrate": 0.55,
        "needs_active": True,
        # dark-blue / navy platinum gradient
        "gradient": "linear-gradient(135deg, #0A1A3A 0%, #1E3A8A 40%, #3B4E8C 70%, #2E1E5A 100%)",
        "glow": "rgba(59,78,140,0.60)",
        "text": "#DCE7FF",
        "border": "#3B4E8C",
    },
    {
        "key": "diamond",
        "name": "Capybara Veteran",
        "tier": "DIAMOND",
        "min_trades": 100,
        "min_winrate": 0.60,
        "needs_active": True,
        # light-blue diamond gradient with shine
        "gradient": "linear-gradient(135deg, #7FE3FF 0%, #B9F2FF 30%, #4FC3F7 60%, #00B4D8 100%)",
        "glow": "rgba(79,195,247,0.70)",
        "text": "#002B3A",
        "border": "#4FC3F7",
    },
]


def _compute_stats(trades):
    """Given a list of trade dicts, return (n_trades, winrate, is_active_7d)."""
    if not trades:
        return 0, 0.0, False
    n = len(trades)
    wins = sum(1 for t in trades if "TP" in str(t.get("result", "")))
    winrate = (wins / n) if n else 0.0
    # active = a trade in the last 7 days
    active = False
    cutoff = datetime.now() - timedelta(days=7)
    for t in trades:
        try:
            d = datetime.strptime(t.get("date", ""), "%d %b %Y")
            if d >= cutoff:
                active = True
                break
        except Exception:
            pass
    return n, winrate, active


def get_rank(trades):
    """Return the highest rank a user currently qualifies for."""
    n, wr, active = _compute_stats(trades or [])
    chosen = RANKS[0]
    for r in RANKS:
        if n < r["min_trades"]:
            continue
        if wr < r["min_winrate"]:
            continue
        if r["needs_active"] and not active:
            continue
        chosen = r
    return chosen


def get_rank_for_user_email(email, registered_users):
    """Lookup a user's rank. Admin always shows Diamond."""
    if email == "admin@bojket.com":
        return RANKS[-1]
    if not email or email not in registered_users:
        return RANKS[0]
    trades = registered_users[email].get("trades", [])
    return get_rank(trades)


def render_rank_badge(rank, size="normal"):
    """Render the rank pill for the topbar. size='normal' | 'small' (for admin list)."""
    if size == "small":
        pad = "3px 10px"
        font = "0.6em"
        emoji_size = "0.95em"
        name_size = "0.55em"
        gap = "6px"
    else:
        pad = "7px 18px"
        font = "0.78em"
        emoji_size = "1.4em"
        name_size = "0.55em"
        gap = "9px"

    return html.Div(
        [
            html.Span("🦫", style={
                "fontSize": emoji_size,
                "filter": "drop-shadow(0 0 4px rgba(0,0,0,0.5))",
                "marginRight": gap,
            }),
            html.Div([
                html.Div(rank["tier"], style={
                    "color": rank["text"],
                    "fontSize": name_size,
                    "fontWeight": "800",
                    "letterSpacing": "2px",
                    "lineHeight": "1",
                    "opacity": "0.85",
                }),
                html.Div(rank["name"], style={
                    "color": rank["text"],
                    "fontSize": font,
                    "fontWeight": "800",
                    "letterSpacing": "0.5px",
                    "lineHeight": "1.2",
                    "marginTop": "2px",
                }),
            ]),
        ],
        id="rank-badge",
        title="Your current rank",
        className="rank-badge-pulse",
        style={
            "background": rank["gradient"],
            "border": f"1.5px solid {rank['border']}",
            "borderRadius": "14px",
            "padding": pad,
            "display": "inline-flex",
            "alignItems": "center",
            "boxShadow": f"0 0 18px {rank['glow']}, inset 0 1px 0 rgba(255,255,255,0.25)",
            "cursor": "default",
            "marginLeft": "10px",
            "transition": "transform 0.2s ease, box-shadow 0.2s ease",
        },
    )