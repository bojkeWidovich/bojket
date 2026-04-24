# =============================================================================
#  pages.py  --  All page layouts + UI component builders
#  Sections: landing, login, onboarding, pricing, dashboard
# =============================================================================

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import (
    PURPLE, PURPLE_LIGHT, PURPLE_GLOW, BG_DARK, BG_CARD, BG_CARD2, BORDER,
    BULL, BEAR, NEUTRAL, TEXT_MAIN, TEXT_DIM, TEXT_MUTED, MA50_COLOR, MA20_COLOR,
    ADMIN_EMAIL, BETA_ACCOUNTS, PLAN_LIMITS, REGISTERED_USERS,
    SYMBOLS, LABELS, ASSET_ICONS, CATEGORY_ICONS, ALL_OPTIONS,
    ALL_PATTERNS, PAT_COLOR, PAT_ABBR, SEN_EMOJI, SEN_LABEL, MAX_IND, DESCS,
)
from ranks import RANKS, render_rank_badge, get_rank, get_rank_for_user_email

def _review_card(initials, name, country_flag, plan, quote, accent=PURPLE, avatar_url=None):
    # Avatar: photo if URL provided, else coloured initials circle
    if avatar_url:
        avatar = html.Img(src=avatar_url, style={
            "width":"44px","height":"44px","borderRadius":"50%",
            "objectFit":"cover","border":f"2px solid {accent}60","flexShrink":"0"})
    else:
        avatar = html.Div(initials, style={
            "width":"44px","height":"44px","borderRadius":"50%",
            "backgroundColor":f"{accent}30","border":f"1px solid {accent}50",
            "color":accent,"fontWeight":"800","fontSize":"0.88em",
            "display":"flex","alignItems":"center","justifyContent":"center","flexShrink":"0"})
    return html.Div([
        html.Div([
            avatar,
            html.Div([
                html.Div(f"{name}  {country_flag}", style={"color":TEXT_MAIN,"fontWeight":"700","fontSize":"0.82em"}),
                html.Div([html.Span(plan, style={"color":TEXT_MUTED,"fontSize":"0.6em","border":f"1px solid {BORDER}",
                    "borderRadius":"20px","padding":"1px 8px"})],style={"marginTop":"2px"}),
            ]),
            html.Div("★★★★★", style={"color":"#facc15","fontSize":"0.75em","marginLeft":"auto","letterSpacing":"1px"}),
        ], style={"display":"flex","alignItems":"center","gap":"12px","marginBottom":"12px"}),
        html.Div(f'"{quote}"', style={"color":"rgba(255,255,255,0.6)","fontSize":"0.84em","lineHeight":"1.65","fontStyle":"italic"}),
    ], style={"backgroundColor":"rgba(255,255,255,0.03)","border":"1px solid rgba(255,255,255,0.07)",
              "borderRadius":"16px","padding":"22px"})


def landing_page():
    # ── all-caps copy system ──
    strings = {
        "tagline":       "THE FUTURE OF TRADING.",
        "signin":        "SIGN IN",
        "lp_badge":      "PRIVATE ACCESS",
        "lp_badge_sub":  "BY INVITATION ONLY",
        "lp_h1":         "EXCLUSIVE TRADING SYSTEM. SERIOUS CAPITAL.",
        "lp_desc":       "INSTITUTIONAL-GRADE SIGNALS. A CLOSED PROGRAM FOR A LIMITED NUMBER OF CLIENTS. LIFETIME ACCESS TO EVERY UPDATE.",
        "lp_cta":        "BOOK A PRIVATE CALL",
        "trust_items":   ["PRIVATE ONBOARDING", "LIFETIME ACCESS", "24/7 DIRECT SUPPORT"],
        "trust_geo":     "TRUSTED BY TRADERS IN GERMANY · SWITZERLAND · AUSTRIA · UK · IRELAND",
        "built_tag":     "THE SYSTEM THAT CHANGED HOW WE TRADE",
        "built_h2":      "BUILT FOR TRADERS WHO ARE DONE GUESSING.",
        "built_sub":     "A COMPLETE TRADING INTELLIGENCE SUITE. USED BY CAPITAL THAT TAKES ITSELF SERIOUSLY.",
        "feat":          [("📊", "MULTI-TIMEFRAME ANALYSIS",  "See what the bigger trend is doing before you enter."),
                          ("🧠", "XGBoost ML ENGINE",          "Trained on 2 years of real data — learns what actually wins."),
                          ("⚡", "DEFINED ENTRY, TP & SL",     "Every signal comes with a precise entry, target, and stop."),
                          ("🤖", "AI TRADING MENTOR",          "Available 24/7. Answers like a trader, not a textbook."),
                          ("🔬", "BACKTESTING ENGINE",         "Validate any strategy against 2 years of market history."),
                          ("📓", "SMART TRADE JOURNAL",        "Every trade logged. Watch your edge sharpen over time.")],
        "footer_copy":   "© 2026 BOJKET  ·  NOT FINANCIAL ADVICE.",
        "footer_sub":    "THE FUTURE OF TRADING.",
    }
    def tr(k): return strings.get(k, k)

    return html.Div([
        html.Div(className="money-field", children=[
            html.Span("$",className="money m1"),html.Span("€",className="money m2"),
            html.Span("$",className="money m3"),html.Span("€",className="money m4"),
            html.Span("$",className="money m5"),html.Span("€",className="money m6"),
            html.Span("$",className="money m7"),html.Span("€",className="money m8"),
            html.Span("$",className="money m9"),html.Span("€",className="money m10"),
            html.Span("$",className="money m11"),html.Span("€",className="money m12"),
        ]),
    
    
        # ── Navbar ───────────────────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Span("BOJKET", style={"color":"white","fontWeight":"900","fontSize":"1.3em","letterSpacing":"6px"}),
                html.Div(tr("tagline"), style={"color":PURPLE_LIGHT,"fontSize":"0.58em","letterSpacing":"3px","fontWeight":"600","marginTop":"3px"}),
            ]),
            html.Div([
                html.A("FOR TEAMS →", href="/for-teams", style={
                    "color":"white","fontSize":"0.82em","fontWeight":"800",
                    "letterSpacing":"3px","textDecoration":"none","marginRight":"18px",
                    "padding":"10px 22px","borderRadius":"9px",
                    "background":"linear-gradient(135deg,#A855F7,#9333EA)",
                    "border":"1px solid rgba(168,85,247,0.7)",
                    "boxShadow":"0 6px 22px rgba(147,51,234,0.45)",
                    "display":"inline-block","transition":"all 0.2s ease",
                }),
                html.A(tr("signin"), href="/login", style={
                    "color":"rgba(255,255,255,0.75)","padding":"9px 22px","fontSize":"0.72em","fontWeight":"700",
                    "letterSpacing":"2.5px","textDecoration":"none","display":"inline-block",
                    "border":"1px solid rgba(255,255,255,0.18)","borderRadius":"8px",
                    "transition":"all 0.2s ease",
                }),
            ], style={"display":"flex","alignItems":"center"}),
        ], style={"display":"flex","justifyContent":"space-between","alignItems":"center",
                  "padding":"22px 64px","borderBottom":"1px solid rgba(255,255,255,0.06)",
                  "position":"sticky","top":"0","backgroundColor":"rgba(6,6,8,0.92)",
                  "zIndex":"100","backdropFilter":"blur(20px)"}),

        # ── Intro Video ─────────────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Div(tr("built_tag"), className="reveal", style={
                    "color": PURPLE_LIGHT, "fontSize": "0.82em", "fontWeight": "800",
                    "letterSpacing": "5px", "textAlign": "center", "marginBottom": "42px",
                }),
            ]),
            html.Div(
                html.Iframe(
                    src="https://www.youtube.com/embed/ChICDNSkdGo?rel=0&modestbranding=1",
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen",
                    style={"width":"100%","aspectRatio":"16/9","border":"none","borderRadius":"18px","display":"block"},
                ),
                className="reveal",
                style={"maxWidth":"960px","margin":"0 auto","borderRadius":"22px","padding":"5px",
                       "background":"linear-gradient(135deg, rgba(147,51,234,0.3), rgba(147,51,234,0.06))",
                       "boxShadow":"0 24px 80px rgba(0,0,0,0.75), 0 0 60px rgba(147,51,234,0.18)"},
            ),
        ], style={"padding":"72px 64px","borderBottom":"1px solid rgba(255,255,255,0.05)","backgroundColor":"#060608"}),

        # ── HERO (big, bold, premium) ───────────────────────────────────────
        html.Div([
            html.Div([
                # Big "PRIVATE ACCESS" badge
                html.Div([
                    html.Span(tr("lp_badge"), style={
                        "color":"white","fontWeight":"900","fontSize":"0.92em","letterSpacing":"5px",
                    }),
                    html.Span("·", style={"color":PURPLE_LIGHT,"margin":"0 14px","fontSize":"0.9em"}),
                    html.Span(tr("lp_badge_sub"), style={
                        "color":"rgba(255,255,255,0.6)","fontWeight":"600","fontSize":"0.75em","letterSpacing":"3px",
                    }),
                ], className="reveal", style={"display":"inline-flex","alignItems":"center","whiteSpace":"nowrap",
                    "backgroundColor":"rgba(147,51,234,0.14)","border":"1px solid rgba(147,51,234,0.5)",
                    "borderRadius":"100px","padding":"12px 28px","marginBottom":"42px",
                    "boxShadow":"0 0 28px rgba(147,51,234,0.22)"}),

                # Main headline — all caps, gigantic, condensed
                html.H1(tr("lp_h1"), className="reveal hero-title", style={
                    "color":"white","fontWeight":"900","fontSize":"4.6em","lineHeight":"1.02",
                    "margin":"0 0 32px 0","letterSpacing":"-2.5px","textTransform":"uppercase",
                    "maxWidth":"780px",
                }),

                # Short tagline
                html.Div(tr("lp_desc"), className="reveal", style={
                    "color":"rgba(255,255,255,0.6)","fontWeight":"600","fontSize":"0.9em",
                    "letterSpacing":"2.5px","lineHeight":"1.9","marginBottom":"44px","maxWidth":"540px",
                    "textTransform":"uppercase",
                }),

                # Big CTA button — unmissable
                html.A(tr("lp_cta"), href="/book-call", className="reveal cta-mega", style={
                    "background":"linear-gradient(135deg,#A855F7,#9333EA)",
                    "color":"white","padding":"22px 52px","borderRadius":"14px",
                    "fontWeight":"800","fontSize":"1.05em","letterSpacing":"3px",
                    "textDecoration":"none","display":"inline-block",
                    "boxShadow":"0 12px 48px rgba(147,51,234,0.55), 0 0 0 1px rgba(168,85,247,0.7) inset",
                    "whiteSpace":"nowrap","transition":"transform 0.2s ease, box-shadow 0.2s ease",
                }),

                html.Div([
                    html.Span("ALREADY HAVE AN ACCOUNT? ", style={"color":"rgba(255,255,255,0.4)","fontSize":"0.72em","letterSpacing":"2px","fontWeight":"600"}),
                    html.A("SIGN IN →", href="/login", style={
                        "color":PURPLE_LIGHT,"fontSize":"0.72em","fontWeight":"700","textDecoration":"none",
                        "letterSpacing":"2px",
                    }),
                ], className="reveal", style={"marginTop":"22px"}),

            ], style={"flex":"1","maxWidth":"700px"}),

            # Right side — signal card (unchanged)
            html.Div([
                html.Img(src="/assets/logo.png", style={"width":"290px","height":"auto","display":"block",
                    "alignSelf":"center","position":"relative","zIndex":"0","mixBlendMode":"screen",
                    "filter":"blur(0.45px) contrast(18) brightness(1.2)","imageRendering":"auto"}),
                html.Div([
                    html.Div([html.Span("🔒  ",style={"fontSize":"0.9em","marginRight":"3px"}),html.Span("CRYPTO · LIVE SIGNAL",style={"color":PURPLE_LIGHT,"fontSize":"0.62em","letterSpacing":"3px","fontWeight":"700"}),html.Div("MEMBERS-ONLY PREVIEW",style={"color":"rgba(255,255,255,0.32)","fontSize":"0.52em","letterSpacing":"2px","marginTop":"2px","fontWeight":"600"})],style={"marginBottom":"14px","paddingBottom":"10px","borderBottom":"1px solid rgba(147,51,234,0.15)"}),
                    html.Div("BUY", style={"color":BULL,"fontWeight":"900","fontSize":"2.8em","letterSpacing":"-1px","lineHeight":"1"}),
                    html.Div("84% ENGINE SCORE", style={"color":TEXT_MUTED,"fontSize":"0.65em","marginTop":"4px","marginBottom":"10px","letterSpacing":"1.5px","fontWeight":"600"}),
                    html.Div(html.Div(style={"width":"84%","background":"linear-gradient(90deg,#34d399,#10b981)","height":"4px","borderRadius":"4px"}),
                        style={"backgroundColor":"#1e1a2e","borderRadius":"4px","height":"4px","marginBottom":"12px"}),
                    html.Div([html.Span("🧠",style={"fontSize":"0.7em","marginRight":"6px"}),
                              html.Span("ML MODEL:",style={"color":TEXT_MUTED,"fontSize":"0.62em","marginRight":"4px","letterSpacing":"1.5px","fontWeight":"700"}),
                              html.Span("BULL 79%",style={"color":BULL,"fontSize":"0.68em","fontWeight":"800","letterSpacing":"1px"})],
                        style={"marginBottom":"16px"}),
                    *[html.Div([html.Span(ic,style={"color":BULL,"fontSize":"0.7em","marginRight":"8px"}),
                                html.Span(lb,style={"color":"rgba(255,255,255,0.5)","fontSize":"0.66em","marginRight":"6px","letterSpacing":"1px","fontWeight":"600"}),
                                html.Span(vl,style={"color":BULL,"fontSize":"0.68em","fontWeight":"700","letterSpacing":"1px"})],
                                style={"marginBottom":"7px","display":"flex"})
                      for ic,lb,vl in [("✅","EMA TREND","BULLISH"),("✅","HIGHER TF","ALIGNED"),("✅","VWAP","ABOVE"),("🔥","DIVERGENCE","BULLISH"),("✅","VOLUME","HIGH")]],
                    html.Div(style={"height":"1px","backgroundColor":"rgba(255,255,255,0.06)","margin":"16px 0"}),
                    html.Div([
                        html.Div([html.Div("TP 🎯",style={"color":TEXT_MUTED,"fontSize":"0.58em","marginBottom":"3px","letterSpacing":"1.5px","fontWeight":"700"}),html.Div("94,820",style={"color":BULL,"fontWeight":"800"})],style={"flex":"1"}),
                        html.Div([html.Div("SL 🛑",style={"color":TEXT_MUTED,"fontSize":"0.58em","marginBottom":"3px","letterSpacing":"1.5px","fontWeight":"700"}),html.Div("91,200",style={"color":BEAR,"fontWeight":"800"})],style={"flex":"1"}),
                    ], style={"display":"flex"}),
                ], style={"background":"linear-gradient(135deg,#0f0e18,#13101f)","border":"1px solid rgba(147,51,234,0.3)",
                          "borderRadius":"20px","padding":"28px","width":"260px","flexShrink":"0",
                          "boxShadow":"0 20px 60px rgba(0,0,0,0.6)","position":"relative","zIndex":"1"}),
            ], className="reveal", style={"display":"flex","flexDirection":"column","alignItems":"center","flexShrink":"0"}),
        ], style={"display":"flex","justifyContent":"space-between","alignItems":"center","gap":"60px",
                  "padding":"80px 64px 100px 64px","maxWidth":"1280px","margin":"0 auto","position":"relative"}),

        # ── Credibility bar (replaces stats) ────────────────────────────────
        html.Div([
            html.Div([
                *[html.Div([
                    html.Span("✓", style={"color":BULL,"fontWeight":"900","fontSize":"1em","marginRight":"10px"}),
                    html.Span(item, style={"color":"white","fontWeight":"700","fontSize":"0.85em","letterSpacing":"3px"}),
                ], style={"display":"flex","alignItems":"center"}) for item in tr("trust_items")],
            ], className="reveal", style={"display":"flex","justifyContent":"center","gap":"52px","flexWrap":"wrap","marginBottom":"24px"}),
            html.Div(tr("trust_geo"), className="reveal", style={
                "color":"rgba(255,255,255,0.4)","fontSize":"0.72em","fontWeight":"600",
                "letterSpacing":"3px","textAlign":"center",
            }),
        ], style={"borderTop":"1px solid rgba(255,255,255,0.05)","borderBottom":"1px solid rgba(255,255,255,0.05)",
                  "padding":"48px 64px","backgroundColor":"rgba(147,51,234,0.04)"}),

        # ── Features ─────────────────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Div(tr("built_tag"), className="reveal", style={"color":PURPLE_LIGHT,"fontSize":"0.8em","fontWeight":"800","letterSpacing":"5px","textAlign":"center","marginBottom":"18px"}),
                html.H2(tr("built_h2"), className="reveal", style={"color":"white","fontWeight":"900","fontSize":"2.8em","textAlign":"center","margin":"0 0 18px 0","letterSpacing":"-1.5px","lineHeight":"1.1","textTransform":"uppercase"}),
                html.P(tr("built_sub"), className="reveal", style={"color":"rgba(255,255,255,0.5)","textAlign":"center","fontSize":"0.88em","fontWeight":"600","letterSpacing":"2.5px","margin":"0 auto 64px auto","maxWidth":"640px","lineHeight":"1.8","textTransform":"uppercase"}),
            ]),
            html.Div([_feature_card(ic,ti,de) for ic,ti,de in tr("feat")],
                className="reveal",
                style={"display":"grid","gridTemplateColumns":"repeat(3,1fr)","gap":"20px","maxWidth":"1100px","margin":"0 auto"}),
        ], style={"padding":"96px 64px","backgroundColor":"#050507","borderTop":"1px solid rgba(255,255,255,0.04)"}),

        # ── Discord Community Section ────────────────────────────────────────
        html.Div([
            html.Div([
                html.Div([
                    html.Div("PRIVATE COMMUNITY", className="reveal", style={
                        "color":"rgba(88,101,242,0.9)","fontSize":"0.78em","fontWeight":"800",
                        "letterSpacing":"4px","marginBottom":"18px",
                    }),
                    html.H2("A COMMUNITY BUILT ON\nEXCLUSIVE ACCESS.", className="reveal", style={
                        "color":"white","fontWeight":"900","fontSize":"2.4em",
                        "letterSpacing":"-1px","lineHeight":"1.1","margin":"0 0 22px 0",
                        "whiteSpace":"pre-line","textTransform":"uppercase",
                    }),
                    html.P("A PRIVATE DISCORD WITH REAL CLIENTS — MARKET INSIGHTS, LIVE SESSIONS, TRADE REVIEWS. NOT PUBLIC.",
                        className="reveal",
                        style={"color":"rgba(255,255,255,0.55)","fontSize":"0.8em","fontWeight":"600",
                               "letterSpacing":"2.5px","lineHeight":"1.9","maxWidth":"440px","margin":"0"}),
                ], style={"flex":"1","paddingRight":"48px"}),
                html.Div([
                    html.Div([
                        html.Img(src="https://cdn.simpleicons.org/discord/ffffff",
                            style={"width":"36px","height":"36px","opacity":"0.9","marginBottom":"20px"}),
                        html.Div("BOJKET COMMUNITY", style={"color":"white","fontWeight":"900","fontSize":"1.05em","letterSpacing":"3px","marginBottom":"8px"}),
                        html.Div("PRIVATE · MEMBERS ONLY", style={"color":"rgba(255,255,255,0.4)","fontSize":"0.7em","marginBottom":"24px","letterSpacing":"2.5px","fontWeight":"700"}),
                        *[html.Div([
                            html.Span(icon, style={"marginRight":"10px","fontSize":"0.95em"}),
                            html.Span(text, style={"color":"rgba(255,255,255,0.72)","fontSize":"0.76em","letterSpacing":"1.5px","fontWeight":"600"}),
                        ], style={"marginBottom":"11px","display":"flex","alignItems":"center"})
                        for icon, text in [
                            ("📊","LIVE MARKET INSIGHTS"),
                            ("🎯","TRADE SETUPS FROM CLIENTS"),
                            ("📅","EXCLUSIVE EVENTS & SESSIONS"),
                            ("🧠","EDUCATION & STRATEGIES"),
                            ("🔔","EARLY SIGNALS & ALERTS"),
                        ]],
                    ], style={"backgroundColor":"rgba(88,101,242,0.07)","border":"1px solid rgba(88,101,242,0.25)",
                              "borderRadius":"18px","padding":"32px","backdropFilter":"blur(10px)"}),
                ], className="reveal", style={"flex":"1","maxWidth":"360px"}),
            ], style={"display":"flex","alignItems":"center","maxWidth":"1000px","margin":"0 auto","gap":"24px"}),
        ], style={"padding":"96px 64px","borderTop":"1px solid rgba(255,255,255,0.04)",
                  "background":"linear-gradient(180deg, rgba(88,101,242,0.04) 0%, transparent 100%)"}),

# ── WHAT IS BOJKET — click to reveal ──────────────────────────────────
        html.Div([
            html.Div([
                html.Div("IN SIMPLE TERMS", className="reveal", style={
                    "color": PURPLE_LIGHT, "fontSize": "0.82em", "fontWeight": "800",
                    "letterSpacing": "5px", "marginBottom": "28px", "textAlign": "center",
                }),
                html.H2("WHAT IS BOJKET?", className="reveal", style={
                    "color": "white", "fontWeight": "900", "fontSize": "2.8em",
                    "margin": "0 0 36px 0", "letterSpacing": "-1.5px",
                    "textAlign": "center", "textTransform": "uppercase",
                }),
                # The button — clicking it reveals the hidden answer below
                html.Div([
                    html.Button([
                        html.Span("TELL ME IN ONE SENTENCE", style={"marginRight":"12px"}),
                        html.Span("→", id="what-is-arrow", style={"transition":"transform 0.3s ease","display":"inline-block"}),
                    ], id="what-is-btn", n_clicks=0, className="reveal cta-mega", style={
                        "background":"transparent",
                        "color":"white","padding":"18px 44px","borderRadius":"14px",
                        "fontWeight":"800","fontSize":"0.92em","letterSpacing":"3px",
                        "border":f"2px solid {PURPLE}","cursor":"pointer",
                        "boxShadow":"0 0 32px rgba(147,51,234,0.25)",
                        "transition":"all 0.25s ease",
                    }),
                ], style={"display":"flex","justifyContent":"center"}),
                # The hidden answer — revealed by callback on click
                html.Div(id="what-is-answer", style={
                    "maxHeight":"0","overflow":"hidden","opacity":"0",
                    "transition":"max-height 0.7s ease, opacity 0.7s ease, margin-top 0.7s ease",
                    "marginTop":"0","maxWidth":"1000px","margin":"0 auto",
                }, children=[
                    html.Div([
                        html.H3([
                            html.Span("BOJKET IS A ", style={"color":"white"}),
                            html.Span("TRADING TOOL", style={
                                "background":"linear-gradient(135deg,#A855F7,#9333EA)",
                                "-webkit-background-clip":"text","-webkit-text-fill-color":"transparent","background-clip":"text",
                            }),
                            html.Span(" THAT USES AN ADVANCED AI ENGINE TO PREDICT MARKETS AND MAKE ", style={"color":"white"}),
                            html.Span("BETTER DECISIONS FOR YOU", style={
                                "background":"linear-gradient(135deg,#A855F7,#9333EA)",
                                "-webkit-background-clip":"text","-webkit-text-fill-color":"transparent","background-clip":"text",
                            }),
                            html.Span(" — OUTGROWING TRADITIONAL TACTICS IN SECONDS.", style={"color":"white"}),
                        ], style={
                            "fontWeight":"900","fontSize":"2.2em","lineHeight":"1.25",
                            "letterSpacing":"-1px","textAlign":"center",
                            "margin":"56px auto 0 auto","textTransform":"uppercase",
                        }),
                        html.Div(style={"width":"60px","height":"3px","background":"linear-gradient(90deg,#A855F7,#9333EA)","borderRadius":"3px","margin":"40px auto 0 auto"}),
                    ]),
                ]),
            ]),
        ], style={
            "padding":"120px 64px","borderTop":"1px solid rgba(255,255,255,0.05)",
            "background":"radial-gradient(circle at 50% 50%, rgba(147,51,234,0.06) 0%, transparent 70%)",
        }),

        # ── Bottom CTA — tight & premium ─────────────────────────────────────
        html.Div([
            html.Div([
                html.Div("THE NEXT STEP", className="reveal", style={
                    "color":PURPLE_LIGHT,"fontSize":"0.82em","fontWeight":"800","letterSpacing":"5px","marginBottom":"24px",
                }),
                html.H2("BOOK A PRIVATE CALL.", className="reveal", style={
                    "color":"white","fontWeight":"900","fontSize":"3.6em","margin":"0 0 22px 0",
                    "letterSpacing":"-2px","lineHeight":"1.05","textTransform":"uppercase",
                }),
                html.Div("ONE CONVERSATION. NO OBLIGATION. WE DECIDE TOGETHER IF IT'S A FIT.",
                    className="reveal",
                    style={"color":"rgba(255,255,255,0.55)","fontSize":"0.85em","fontWeight":"600",
                           "letterSpacing":"3px","marginBottom":"44px","lineHeight":"1.9"}),
                html.A("BOOK A PRIVATE CALL", href="/book-call", className="reveal cta-mega", style={
                    "background":"linear-gradient(135deg,#A855F7,#9333EA)",
                    "color":"white","padding":"22px 52px","borderRadius":"14px",
                    "fontWeight":"800","fontSize":"1.05em","letterSpacing":"3px",
                    "textDecoration":"none","display":"inline-block",
                    "boxShadow":"0 12px 48px rgba(147,51,234,0.55), 0 0 0 1px rgba(168,85,247,0.7) inset",
                    "whiteSpace":"nowrap",
                }),
            ], style={"textAlign":"center"}),
        ], style={"padding":"120px 64px","borderTop":"1px solid rgba(255,255,255,0.05)"}),

        # ── Our socials ──────────────────────────────────────────────────────
        html.Div([
            html.Div("OUR SOCIALS", className="reveal", style={
                "color":PURPLE_LIGHT,"fontSize":"0.75em","fontWeight":"800",
                "letterSpacing":"5px","textAlign":"center","marginBottom":"28px",
            }),
            html.Div([
                html.A(
                    html.Img(src="https://cdn.simpleicons.org/x/ffffff",
                            style={"width":"26px","height":"26px","opacity":"0.9"}),
                    href="https://x.com/bojkett", target="_blank",
                    className="social-icon-link",
                    title="Follow on X",
                    style={"width":"60px","height":"60px","display":"flex","alignItems":"center","justifyContent":"center",
                           "borderRadius":"50%","backgroundColor":"rgba(255,255,255,0.04)",
                           "border":"1px solid rgba(168,85,247,0.3)","transition":"all 0.25s ease"}),
                html.A(
                    html.Img(src="https://cdn.simpleicons.org/instagram/ffffff",
                            style={"width":"26px","height":"26px","opacity":"0.9"}),
                    href="https://www.instagram.com/bojkett/", target="_blank",
                    className="social-icon-link",
                    title="Follow on Instagram",
                    style={"width":"60px","height":"60px","display":"flex","alignItems":"center","justifyContent":"center",
                           "borderRadius":"50%","backgroundColor":"rgba(255,255,255,0.04)",
                           "border":"1px solid rgba(168,85,247,0.3)","transition":"all 0.25s ease","margin":"0 18px"}),
                html.A(
                    html.Img(src="https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/linkedin.svg",
                            style={"width":"26px","height":"26px","opacity":"0.9"}),
                    href="https://www.linkedin.com/in/bojke-vidovic-5710303b4/", target="_blank",
                    className="social-icon-link",
                    title="Connect on LinkedIn",
                    style={"width":"60px","height":"60px","display":"flex","alignItems":"center","justifyContent":"center",
                           "borderRadius":"50%","backgroundColor":"rgba(255,255,255,0.04)",
                           "border":"1px solid rgba(168,85,247,0.3)","transition":"all 0.25s ease"}),
            ], className="reveal", style={"display":"flex","justifyContent":"center","alignItems":"center"}),
        ], style={"padding":"70px 64px","borderTop":"1px solid rgba(255,255,255,0.05)","textAlign":"center"}),
        # ── Footer ────────────────────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Div("BOJKET", style={"color":"white","fontWeight":"900","fontSize":"1em","letterSpacing":"5px","marginBottom":"4px"}),
                html.Div(tr("footer_sub"), style={"color":TEXT_MUTED,"fontSize":"0.68em","letterSpacing":"2px","fontWeight":"600"}),
            ], style={"flex":"1"}),
            html.Div([
                html.Span("📍", style={"fontSize":"0.9em","marginRight":"7px"}),
                html.Span("BASED IN VIENNA, AUSTRIA", style={"color":"white","fontWeight":"700","fontSize":"0.72em","letterSpacing":"2.5px"}),
            ], style={"flex":"1","display":"flex","alignItems":"center","justifyContent":"center"}),
            html.Div([
                html.Div(tr("footer_copy"), style={"color":TEXT_MUTED,"fontSize":"0.68em","letterSpacing":"2px","fontWeight":"600","marginBottom":"6px"}),
                html.A("contact@bojket.com", href="mailto:contact@bojket.com", style={"color":PURPLE_LIGHT,"fontSize":"0.72em","letterSpacing":"2px","fontWeight":"700","textDecoration":"none"}),
            ], style={"flex":"1","textAlign":"right"}),
        ], style={"display":"flex","justifyContent":"space-between","alignItems":"center","padding":"32px 64px","borderTop":"1px solid rgba(255,255,255,0.05)"}),
    ], style={"backgroundColor":BG_DARK,"minHeight":"100vh","color":TEXT_MAIN,"position":"relative","overflow":"hidden"})

def book_call_page():
    """Cal.com-embedded booking page for private calls."""
    return html.Div([
        html.Div(className="hero-glow"),

        # ── Navbar ──────────────────────────────────────────────────────────
        html.Div([
            html.A([
                html.Span("BOJKET", style={
                    "background":"linear-gradient(135deg,#ffffff 0%,#A855F7 100%)",
                    "-webkit-background-clip":"text","-webkit-text-fill-color":"transparent","background-clip":"text",
                    "fontWeight":"900","fontSize":"1.3em","letterSpacing":"6px",
                }),
                html.Div("THE FUTURE OF TRADING.", style={
                    "color":PURPLE_LIGHT,"fontSize":"0.55em","letterSpacing":"3px","marginTop":"3px","fontWeight":"700",
                }),
            ], href="/", style={"textDecoration":"none"}),
            html.A("← BACK", href="/", style={
                "color":"rgba(255,255,255,0.6)","fontSize":"0.72em","fontWeight":"700",
                "letterSpacing":"2.5px","textDecoration":"none",
            }),
        ], style={"display":"flex","justifyContent":"space-between","alignItems":"center",
                  "padding":"22px 64px","borderBottom":"1px solid rgba(255,255,255,0.06)",
                  "position":"sticky","top":"0","backgroundColor":"rgba(6,6,8,0.92)",
                  "zIndex":"100","backdropFilter":"blur(20px)"}),

        # ── Hero ────────────────────────────────────────────────────────────
        html.Div([
            html.Div("BOOK A PRIVATE CALL", className="reveal", style={
                "color":PURPLE_LIGHT,"fontSize":"0.82em","fontWeight":"800",
                "letterSpacing":"5px","marginBottom":"22px","textAlign":"center",
            }),
            html.H1("Let's have a real conversation.", className="reveal", style={
                "color":"white","fontWeight":"900","fontSize":"2.8em","lineHeight":"1.1",
                "letterSpacing":"-1.5px","margin":"0 auto 20px auto","maxWidth":"780px",
                "textAlign":"center",
            }),
            html.Div("30 minutes. No sales pitch. We figure out if Bojket is the right fit — solo trader or firm.",
                className="reveal", style={
                    "color":"rgba(255,255,255,0.6)","fontSize":"1em","fontWeight":"500",
                    "lineHeight":"1.7","maxWidth":"600px","margin":"0 auto 50px auto",
                    "textAlign":"center","fontStyle":"italic",
                }),

            # ── Cal.com embed ────────────────────────────────────────────────
            html.Div(
                html.Iframe(
                    src="https://cal.com/bojket/private-call?embed=true&theme=dark",
                    style={"width":"100%","height":"760px","border":"none","borderRadius":"16px","display":"block","backgroundColor":"#0a0910"},
                    allow="camera; microphone; autoplay; encrypted-media; fullscreen; payment",
                ),
                className="reveal",
                style={
                    "maxWidth":"960px","margin":"0 auto","borderRadius":"20px","padding":"4px",
                    "background":"linear-gradient(135deg, rgba(147,51,234,0.35), rgba(147,51,234,0.08))",
                    "boxShadow":"0 24px 80px rgba(0,0,0,0.75), 0 0 60px rgba(147,51,234,0.18)",
                },
            ),

            # ── Small reassurance line below calendar ───────────────────────
            html.Div([
                html.Span("🔒  ", style={"marginRight":"4px"}),
                html.Span("All calls are private and confidential.", style={
                    "color":"rgba(255,255,255,0.45)","fontSize":"0.85em","fontWeight":"500","fontStyle":"italic",
                }),
            ], className="reveal", style={"textAlign":"center","marginTop":"36px"}),
            html.Div("Can't see the calendar? ", className="reveal", style={
                "color":"rgba(255,255,255,0.4)","fontSize":"0.82em","textAlign":"center","marginTop":"8px",
                "display":"inline-block","width":"100%",
            }),
      html.Div(
                html.A("Open calendar in a new window →", href="https://cal.com/bojket/private-call", target="_blank", style={
                    "color":PURPLE_LIGHT,"fontSize":"0.82em","fontWeight":"700","textDecoration":"none","letterSpacing":"0.5px",
                }),
                className="reveal", style={"textAlign":"center","marginTop":"4px","marginBottom":"14px"}
            ),
            html.Div([
                html.Span("Prefer email? ", style={"color":"rgba(255,255,255,0.4)","fontSize":"0.82em","fontWeight":"500"}),
                html.A("contact@bojket.com", href="mailto:contact@bojket.com", style={"color":PURPLE_LIGHT,"fontSize":"0.82em","fontWeight":"700","textDecoration":"none","letterSpacing":"0.5px"}),
            ], className="reveal", style={"textAlign":"center","marginBottom":"40px"}),

        ], style={"padding":"72px 24px 80px 24px","maxWidth":"1200px","margin":"0 auto"}),

        # ── Trust strip ─────────────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Div([
                    html.Div(icon, style={"fontSize":"1.4em","marginBottom":"10px"}),
                    html.Div(title, style={"color":"white","fontWeight":"800","fontSize":"0.85em","letterSpacing":"1.5px","marginBottom":"6px"}),
                    html.Div(desc, style={"color":"rgba(255,255,255,0.5)","fontSize":"0.78em","lineHeight":"1.6"}),
                ], style={"flex":"1","textAlign":"center"})
                for icon, title, desc in [
                    ("🎯", "No Pressure", "If it's not a fit, we both move on."),
                    ("⏱", "30 Minutes", "Enough time to get to the real question."),
                    ("🤝", "Founder-Led", "You'll be talking to me directly."),
                ]
            ], className="reveal", style={"display":"flex","gap":"32px","maxWidth":"900px","margin":"0 auto"}),
        ], style={"borderTop":"1px solid rgba(255,255,255,0.05)","padding":"48px 64px","backgroundColor":"rgba(147,51,234,0.03)"}),

        # ── Footer ──────────────────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Div("BOJKET", style={"color":"white","fontWeight":"900","fontSize":"1em","letterSpacing":"5px","marginBottom":"4px"}),
                html.Div("THE FUTURE OF TRADING.", style={"color":TEXT_MUTED,"fontSize":"0.68em","letterSpacing":"2px","fontWeight":"600"}),
            ], style={"flex":"1"}),
            html.Div([
                html.Span("📍", style={"fontSize":"0.9em","marginRight":"7px"}),
             html.Span("BASED IN VIENNA, AUSTRIA", style={"color":"white","fontWeight":"700","fontSize":"0.72em","letterSpacing":"2.5px"}),
            ], style={"flex":"1","display":"flex","alignItems":"center","justifyContent":"center"}),
            html.Div([
                html.Div("© 2026 BOJKET  ·  NOT FINANCIAL ADVICE.", style={"color":TEXT_MUTED,"fontSize":"0.68em","letterSpacing":"2px","fontWeight":"600","marginBottom":"6px"}),
                html.A("contact@bojket.com", href="mailto:contact@bojket.com", style={"color":PURPLE_LIGHT,"fontSize":"0.72em","letterSpacing":"2px","fontWeight":"700","textDecoration":"none"}),
            ], style={"flex":"1","textAlign":"right"}),
        ], style={"display":"flex","justifyContent":"space-between","alignItems":"center","padding":"32px 64px","borderTop":"1px solid rgba(255,255,255,0.05)"}),

    ], style={"backgroundColor":BG_DARK,"minHeight":"100vh","color":TEXT_MAIN,"position":"relative","overflow":"hidden"})
    """Enterprise landing: prop firms, family offices, crypto funds."""
    tiers = [
        {
            "name": "TEAM",
            "price": "€15,000",
            "period": "/ year",
            "seats": "Up to 5 traders",
            "desc": "Small desks. Emerging firms.",
            "features": [
                "5 full-access seats",
                "Per-trader analytics",
                "Priority support",
                "Audit log & CSV export",
                "Private Discord",
                "Lifetime platform updates",
            ],
            "highlight": False,
        },
        {
            "name": "FIRM",
            "price": "€45,000",
            "period": "/ year",
            "seats": "Up to 25 traders",
            "desc": "Established firms. Active capital.",
            "features": [
                "25 full-access seats",
                "Multi-trader admin",
                "REST API access",
                "Dedicated account manager",
                "Custom signal calibration",
                "Quarterly strategy reviews",
                "SLA-backed response times",
            ],
            "highlight": True,
        },
        {
            "name": "ENTERPRISE",
            "price": "Custom",
            "period": "",
            "seats": "50+ traders",
            "desc": "Institutional capital. Scale.",
            "features": [
                "Unlimited seats",
                "Private deployment option",
                "Custom compliance features",
                "Direct founder access",
                "On-site or virtual onboarding",
                "Full data residency control",
            ],
            "highlight": False,
        },
    ]

    def tier_card(t):
        bg = "linear-gradient(135deg,#12102a,#1a1238)" if t["highlight"] else "#0a0910"
        border = f"2px solid {PURPLE}" if t["highlight"] else "1px solid rgba(255,255,255,0.08)"
        glow = "0 0 60px rgba(147,51,234,0.35)" if t["highlight"] else "none"
        return html.Div([
            *([html.Div("MOST POPULAR", style={
                "position":"absolute","top":"-12px","left":"50%","transform":"translateX(-50%)",
                "background":"linear-gradient(135deg,#A855F7,#9333EA)","color":"white",
                "fontSize":"0.62em","fontWeight":"900","letterSpacing":"3px",
                "padding":"5px 16px","borderRadius":"100px","whiteSpace":"nowrap",
                "boxShadow":"0 4px 16px rgba(147,51,234,0.5)",
            })] if t["highlight"] else []),
            html.Div(t["name"], style={
                "color":PURPLE_LIGHT if t["highlight"] else "rgba(255,255,255,0.55)",
                "fontSize":"0.78em","fontWeight":"800","letterSpacing":"4px","marginBottom":"14px",
            }),
            html.Div([
                html.Span(t["price"], style={"color":"white","fontWeight":"900","fontSize":"2.4em","letterSpacing":"-1.5px"}),
                html.Span(t["period"], style={"color":"rgba(255,255,255,0.4)","fontSize":"0.9em","marginLeft":"6px","fontWeight":"600"}),
            ], style={"marginBottom":"4px"}),
            html.Div(t["seats"], style={
                "color":"rgba(255,255,255,0.55)","fontSize":"0.74em","fontWeight":"700",
                "letterSpacing":"1.5px","marginBottom":"10px","textTransform":"uppercase",
            }),
            html.Div(t["desc"], style={
                "color":"rgba(255,255,255,0.72)","fontSize":"0.88em","marginBottom":"22px","fontStyle":"italic",
            }),
            html.Div(style={"height":"1px","background":"rgba(255,255,255,0.08)","marginBottom":"22px"}),
            *[html.Div([
                html.Span("✓", style={"color":BULL,"fontWeight":"900","marginRight":"10px","flexShrink":"0"}),
                html.Span(f, style={"color":"rgba(255,255,255,0.85)","fontSize":"0.86em","lineHeight":"1.5"}),
            ], style={"display":"flex","alignItems":"flex-start","marginBottom":"10px"}) for f in t["features"]],
            html.A("Request a Call →", href="/book-call?source=enterprise", style={
                "display":"block","width":"100%","textAlign":"center","padding":"14px",
                "marginTop":"26px","borderRadius":"11px",
                "background":"linear-gradient(135deg,#A855F7,#9333EA)" if t["highlight"] else "transparent",
                "border":"2px solid " + (PURPLE if t["highlight"] else "rgba(168,85,247,0.4)"),
                "color":"white","fontWeight":"800","fontSize":"0.82em","letterSpacing":"2px",
                "textDecoration":"none","boxShadow":"0 8px 28px rgba(147,51,234,0.4)" if t["highlight"] else "none",
                "transition":"all 0.2s ease",
            }),
        ], className="reveal plan-card", style={
            "background":bg,"border":border,"borderRadius":"20px",
            "padding":"38px 30px","flex":"1","maxWidth":"340px",
            "boxShadow":glow,"position":"relative",
        })

    return html.Div([
        html.Div(className="hero-glow"),

        # ── Navbar ──────────────────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Span("BOJKET", style={
                    "background":"linear-gradient(135deg,#ffffff 0%,#A855F7 100%)",
                    "-webkit-background-clip":"text","-webkit-text-fill-color":"transparent","background-clip":"text",
                    "fontWeight":"900","fontSize":"1.3em","letterSpacing":"6px",
                }),
                html.Div("FOR TEAMS & INSTITUTIONS", style={
                    "color":PURPLE_LIGHT,"fontSize":"0.55em","letterSpacing":"3px","marginTop":"3px","fontWeight":"700",
                }),
            ]),
            html.Div([
                html.A("SOLO", href="/", style={
                    "color":"rgba(255,255,255,0.55)","fontSize":"0.72em","fontWeight":"700","letterSpacing":"2.5px",
                    "textDecoration":"none","marginRight":"20px",
                }),
                html.A("SIGN IN", href="/login", style={
                    "color":"rgba(255,255,255,0.75)","padding":"9px 22px","fontSize":"0.72em","fontWeight":"700",
                    "letterSpacing":"2.5px","textDecoration":"none","display":"inline-block",
                    "border":"1px solid rgba(255,255,255,0.18)","borderRadius":"8px",
                }),
            ], style={"display":"flex","alignItems":"center"}),
        ], style={"display":"flex","justifyContent":"space-between","alignItems":"center",
                  "padding":"22px 64px","borderBottom":"1px solid rgba(255,255,255,0.06)",
                  "position":"sticky","top":"0","backgroundColor":"rgba(6,6,8,0.92)",
                  "zIndex":"100","backdropFilter":"blur(20px)"}),

        # ── Hero ────────────────────────────────────────────────────────────
        html.Div([
            html.Div("FOR TEAMS", className="reveal", style={
                "color":PURPLE_LIGHT,"fontSize":"0.85em","fontWeight":"800",
                "letterSpacing":"5px","marginBottom":"26px",
            }),
            html.H1("Built for firms that trade seriously.", className="reveal", style={
                "color":"white","fontWeight":"900","fontSize":"3.6em","lineHeight":"1.08",
                "letterSpacing":"-2px","margin":"0 0 26px 0","maxWidth":"860px",
            }),
            html.Div("Multi-seat access. Admin controls. API integration. Direct line to the founder.",
                className="reveal", style={
                    "color":"rgba(255,255,255,0.65)","fontSize":"1.05em","fontWeight":"500",
                    "lineHeight":"1.7","maxWidth":"640px","marginBottom":"40px",
                }),
            html.A("Book a Private Call →", href="/book-call?source=enterprise", className="reveal cta-mega", style={
                "background":"linear-gradient(135deg,#A855F7,#9333EA)",
                "color":"white","padding":"20px 48px","borderRadius":"14px",
                "fontWeight":"800","fontSize":"1em","letterSpacing":"2px",
                "textDecoration":"none","display":"inline-block",
                "boxShadow":"0 12px 48px rgba(147,51,234,0.55), 0 0 0 1px rgba(168,85,247,0.7) inset",
            }),
        ], style={"padding":"80px 64px 56px 64px","maxWidth":"1200px","margin":"0 auto"}),

        # ── Trust strip (simple, 4 points) ──────────────────────────────────
        html.Div([
            html.Div([
                html.Div([
                    html.Div(icon, style={"fontSize":"1.4em","marginBottom":"10px"}),
                    html.Div(title, style={"color":"white","fontWeight":"800","fontSize":"0.88em","letterSpacing":"1.5px","marginBottom":"6px"}),
                    html.Div(desc, style={"color":"rgba(255,255,255,0.5)","fontSize":"0.78em","lineHeight":"1.6"}),
                ], style={"flex":"1","textAlign":"center"})
                for icon, title, desc in [
                    ("🔒", "Private & Secure", "Your signals stay yours."),
                    ("⚡", "Institutional-Grade", "10-factor engine, ML, backtesting."),
                    ("🛠", "Hands-On Support", "Direct line to the founder."),
                    ("📊", "Audit-Ready", "Full logs. CSV export."),
                ]
            ], className="reveal", style={"display":"flex","gap":"32px","maxWidth":"1100px","margin":"0 auto"}),
        ], style={"borderTop":"1px solid rgba(255,255,255,0.05)","borderBottom":"1px solid rgba(255,255,255,0.05)",
                  "padding":"44px 64px","backgroundColor":"rgba(147,51,234,0.03)"}),

        # ── Pricing ─────────────────────────────────────────────────────────
        html.Div([
            html.Div("PRICING", className="reveal", style={
                "color":PURPLE_LIGHT,"fontSize":"0.8em","fontWeight":"800","letterSpacing":"5px",
                "textAlign":"center","marginBottom":"16px",
            }),
            html.H2("Simple. Transparent. Real value.", className="reveal", style={
                "color":"white","fontWeight":"900","fontSize":"2.4em","textAlign":"center",
                "margin":"0 0 14px 0","letterSpacing":"-1.5px",
            }),
            html.Div("Every engagement starts with a private call. No surprises.",
                className="reveal", style={
                    "color":"rgba(255,255,255,0.5)","fontSize":"0.96em","textAlign":"center","marginBottom":"60px","fontStyle":"italic",
                }),
            html.Div([tier_card(t) for t in tiers],
                style={"display":"flex","gap":"24px","justifyContent":"center","flexWrap":"wrap","maxWidth":"1200px","margin":"0 auto"}),

            # White-label add-on banner
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("🎨  ", style={"fontSize":"1.3em","marginRight":"4px"}),
                        html.Span("WHITE LABEL AVAILABLE", style={
                            "color":PURPLE_LIGHT,"fontSize":"0.82em","fontWeight":"800","letterSpacing":"3px",
                        }),
                    ], style={"marginBottom":"10px","display":"flex","alignItems":"center","justifyContent":"center"}),
                    html.Div("Your logo. Your name. Your domain. Your brand.", style={
                        "color":"white","fontSize":"1.25em","fontWeight":"800","marginBottom":"10px","letterSpacing":"-0.5px",
                    }),
                    html.Div("White-labeling is an add-on to any tier. Pricing is customised to your firm, scope, and timeline.", style={
                        "color":"rgba(255,255,255,0.6)","fontSize":"0.9em","lineHeight":"1.65","maxWidth":"640px","margin":"0 auto",
                    }),
                ], style={"textAlign":"center"}),
            ], className="reveal", style={
                "maxWidth":"780px","margin":"56px auto 0 auto","padding":"32px 28px",
                "background":"linear-gradient(135deg, rgba(147,51,234,0.07), rgba(147,51,234,0.02))",
                "border":"1px solid rgba(147,51,234,0.3)","borderRadius":"18px",
            }),
        ], style={"padding":"92px 64px","backgroundColor":"#050507","borderTop":"1px solid rgba(255,255,255,0.04)"}),

        # ── What your firm gets (simplified to 6 cards, short copy) ────────
        html.Div([
            html.Div("WHAT YOUR FIRM GETS", className="reveal", style={
                "color":PURPLE_LIGHT,"fontSize":"0.8em","fontWeight":"800","letterSpacing":"5px",
                "textAlign":"center","marginBottom":"16px",
            }),
            html.H2("Everything your traders need.", className="reveal", style={
                "color":"white","fontWeight":"900","fontSize":"2.3em","textAlign":"center",
                "margin":"0 0 52px 0","letterSpacing":"-1.5px",
            }),
            html.Div([
                html.Div([
                    html.Div(icon, style={"fontSize":"2em","marginBottom":"14px"}),
                    html.Div(title, style={"color":"white","fontWeight":"800","fontSize":"1em","marginBottom":"8px","letterSpacing":"0.4px"}),
                    html.Div(desc, style={"color":"rgba(255,255,255,0.55)","fontSize":"0.86em","lineHeight":"1.65"}),
                ], className="reveal feature-card", style={
                    "background":"rgba(147,51,234,0.06)","border":"1px solid rgba(255,255,255,0.07)",
                    "borderRadius":"16px","padding":"26px","flex":"1","minWidth":"270px",
                })
                for icon, title, desc in [
                    ("👥", "Multi-Seat Admin", "One dashboard controls every trader. Add, remove, audit — in seconds."),
                    ("🔌", "REST API Access", "Pipe signals into your OMS, Slack, or internal tools."),
                    ("📈", "Per-Trader Analytics", "Every trader's win rate, streaks, and top assets — in one view."),
                    ("📑", "Audit Logs & Export", "Every signal, trade, and login. CSV-ready."),
                    ("🎯", "Signal Calibration", "Tune the engine to your firm's strategy. Weight factors. Set thresholds."),
                    ("🎨", "White Label Option", "Custom logo, name, colors, domain. Make it yours."),
                ]
            ], style={"display":"grid","gridTemplateColumns":"repeat(auto-fit, minmax(270px, 1fr))","gap":"20px","maxWidth":"1100px","margin":"0 auto"}),
        ], style={"padding":"92px 64px","borderTop":"1px solid rgba(255,255,255,0.04)"}),

        # ── Founder partnership — NEW section ──────────────────────────────
        html.Div([
            html.Div([
                html.Div("DIRECT FOUNDER ACCESS", className="reveal", style={
                    "color":PURPLE_LIGHT,"fontSize":"0.8em","fontWeight":"800","letterSpacing":"5px","marginBottom":"18px",
                }),
                html.H2("You're not talking to a support ticket.", className="reveal", style={
                    "color":"white","fontWeight":"900","fontSize":"2.3em","margin":"0 0 22px 0","letterSpacing":"-1.5px","lineHeight":"1.15",
                }),
                html.Div([
                    html.P("Every firm that joins Bojket gets a direct line to me — the founder. Not a chatbot. Not a junior CS rep. Me.", style={
                        "color":"rgba(255,255,255,0.78)","fontSize":"1.02em","lineHeight":"1.8","marginBottom":"14px",
                    }),
                    html.P("We stay in constant communication. Feature requests go straight to the roadmap. Bugs get my attention the same day. Your firm's edge becomes my job.", style={
                        "color":"rgba(255,255,255,0.62)","fontSize":"0.95em","lineHeight":"1.8","marginBottom":"14px",
                    }),
                    html.P("This isn't a SaaS subscription. It's a partnership — built on satisfaction, iteration, and real relationships.", style={
                        "color":"rgba(255,255,255,0.55)","fontSize":"0.92em","lineHeight":"1.8","fontStyle":"italic",
                    }),
                ], className="reveal"),
                html.Div([
                    *[html.Div([
                        html.Span("→  ", style={"color":PURPLE_LIGHT,"fontWeight":"900","marginRight":"4px"}),
                        html.Span(point, style={"color":"rgba(255,255,255,0.8)","fontSize":"0.9em","fontWeight":"600","letterSpacing":"0.3px"}),
                    ], style={"marginBottom":"10px"}) for point in [
                        "Dedicated WhatsApp / Signal / Discord channel with me",
                        "Monthly check-ins to review what's working",
                        "Feature requests built on your timeline",
                        "Zero-bureaucracy support — one message, one response",
                    ]],
                ], className="reveal", style={"marginTop":"30px"}),
            ], style={"maxWidth":"820px","margin":"0 auto"}),
        ], style={"padding":"92px 64px","borderTop":"1px solid rgba(255,255,255,0.04)",
                  "backgroundColor":"rgba(147,51,234,0.03)"}),

        # ── Who it's for ────────────────────────────────────────────────────
        html.Div([
            html.Div("WHO IT'S FOR", className="reveal", style={
                "color":PURPLE_LIGHT,"fontSize":"0.8em","fontWeight":"800","letterSpacing":"5px",
                "textAlign":"center","marginBottom":"16px",
            }),
            html.H2("Serious capital. Serious tools.", className="reveal", style={
                "color":"white","fontWeight":"900","fontSize":"2.3em","textAlign":"center",
                "margin":"0 0 52px 0","letterSpacing":"-1.5px",
            }),
            html.Div([
                html.Div([
                    html.Div(label, style={"color":PURPLE_LIGHT,"fontWeight":"800","fontSize":"0.72em","letterSpacing":"3px","marginBottom":"12px"}),
                    html.Div(title, style={"color":"white","fontWeight":"800","fontSize":"1.2em","marginBottom":"12px","lineHeight":"1.3"}),
                    html.Div(desc, style={"color":"rgba(255,255,255,0.6)","fontSize":"0.88em","lineHeight":"1.7"}),
                ], className="reveal", style={
                    "flex":"1","minWidth":"260px","padding":"30px 26px",
                    "background":"linear-gradient(180deg, rgba(147,51,234,0.04), transparent)",
                    "border":"1px solid rgba(147,51,234,0.18)","borderRadius":"16px",
                })
                for label, title, desc in [
                    ("PROP FIRMS", "Prop Trading Firms", "Give every trader an institutional edge. Track the desk. Scale without analysts."),
                    ("FAMILY OFFICES", "Family Offices", "Pro-grade intelligence without Bloomberg's price tag. Private. Yours."),
                    ("CRYPTO FUNDS", "Crypto Hedge Funds", "Built for 24/7 markets. ML learns your asset class. Backtested."),
                ]
            ], style={"display":"flex","gap":"22px","flexWrap":"wrap","maxWidth":"1100px","margin":"0 auto"}),
        ], style={"padding":"92px 64px","borderTop":"1px solid rgba(255,255,255,0.04)","backgroundColor":"rgba(147,51,234,0.02)"}),

        # ── Bottom CTA ──────────────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Div("THE NEXT STEP", className="reveal", style={
                    "color":PURPLE_LIGHT,"fontSize":"0.82em","fontWeight":"800","letterSpacing":"5px","marginBottom":"22px",
                }),
                html.H2("Talk to the founder.", className="reveal", style={
                    "color":"white","fontWeight":"900","fontSize":"3em","margin":"0 0 20px 0",
                    "letterSpacing":"-2px","lineHeight":"1.08",
                }),
                html.Div("One call. No sales deck. We figure out if Bojket fits your firm — together.",
                    className="reveal",
                    style={"color":"rgba(255,255,255,0.6)","fontSize":"1em","marginBottom":"40px","lineHeight":"1.75","fontStyle":"italic"}),
                html.A("Book a Private Call →", href="/book-call?source=enterprise", className="reveal cta-mega", style={
                    "background":"linear-gradient(135deg,#A855F7,#9333EA)",
                    "color":"white","padding":"22px 52px","borderRadius":"14px",
                    "fontWeight":"800","fontSize":"1.02em","letterSpacing":"2px",
                    "textDecoration":"none","display":"inline-block",
                    "boxShadow":"0 12px 48px rgba(147,51,234,0.55), 0 0 0 1px rgba(168,85,247,0.7) inset",
                }),
            ], style={"textAlign":"center"}),
        ], style={"padding":"110px 64px","borderTop":"1px solid rgba(255,255,255,0.05)"}),

        # ── Footer ──────────────────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Div("BOJKET", style={"color":"white","fontWeight":"900","fontSize":"1em","letterSpacing":"5px","marginBottom":"4px"}),
                html.Div("THE FUTURE OF TRADING.", style={"color":TEXT_MUTED,"fontSize":"0.68em","letterSpacing":"2px","fontWeight":"600"}),
            ], style={"flex":"1"}),
            html.Div([
                html.Span("📍", style={"fontSize":"0.9em","marginRight":"7px"}),
                html.Span("BASED IN VIENNA, AUSTRIA", style={"color":"white","fontWeight":"700","fontSize":"0.72em","letterSpacing":"2.5px"}),
            ], style={"flex":"1","display":"flex","alignItems":"center","justifyContent":"center"}),
            html.Div("© 2026 BOJKET  ·  NOT FINANCIAL ADVICE.", style={"color":TEXT_MUTED,"fontSize":"0.68em","letterSpacing":"2px","fontWeight":"600","flex":"1","textAlign":"right"}),
        ], style={"display":"flex","justifyContent":"space-between","alignItems":"center","padding":"32px 64px","borderTop":"1px solid rgba(255,255,255,0.05)"}),

    ], style={"backgroundColor":BG_DARK,"minHeight":"100vh","color":TEXT_MAIN,"position":"relative","overflow":"hidden"})

def for_teams_page():
    """Enterprise landing: prop firms, family offices, crypto funds."""
    tiers = [
        {
            "name": "TEAM",
            "price": "€15,000",
            "period": "/ year",
            "seats": "Up to 5 traders",
            "desc": "Small desks. Emerging firms.",
            "features": [
                "5 full-access seats",
                "Per-trader analytics",
                "Priority support",
                "Audit log & CSV export",
                "Private Discord",
                "Lifetime platform updates",
            ],
            "highlight": False,
        },
        {
            "name": "FIRM",
            "price": "€45,000",
            "period": "/ year",
            "seats": "Up to 25 traders",
            "desc": "Established firms. Active capital.",
            "features": [
                "25 full-access seats",
                "Multi-trader admin",
                "REST API access",
                "Dedicated account manager",
                "Custom signal calibration",
                "Quarterly strategy reviews",
                "SLA-backed response times",
            ],
            "highlight": True,
        },
        {
            "name": "ENTERPRISE",
            "price": "Custom",
            "period": "",
            "seats": "50+ traders",
            "desc": "Institutional capital. Scale.",
            "features": [
                "Unlimited seats",
                "Private deployment option",
                "Custom compliance features",
                "Direct founder access",
                "On-site or virtual onboarding",
                "Full data residency control",
            ],
            "highlight": False,
        },
    ]

    def tier_card(t):
        bg = "linear-gradient(135deg,#12102a,#1a1238)" if t["highlight"] else "#0a0910"
        border = f"2px solid {PURPLE}" if t["highlight"] else "1px solid rgba(255,255,255,0.08)"
        glow = "0 0 60px rgba(147,51,234,0.35)" if t["highlight"] else "none"
        return html.Div([
            *([html.Div("MOST POPULAR", style={
                "position":"absolute","top":"-12px","left":"50%","transform":"translateX(-50%)",
                "background":"linear-gradient(135deg,#A855F7,#9333EA)","color":"white",
                "fontSize":"0.62em","fontWeight":"900","letterSpacing":"3px",
                "padding":"5px 16px","borderRadius":"100px","whiteSpace":"nowrap",
                "boxShadow":"0 4px 16px rgba(147,51,234,0.5)",
            })] if t["highlight"] else []),
            html.Div(t["name"], style={
                "color":PURPLE_LIGHT if t["highlight"] else "rgba(255,255,255,0.55)",
                "fontSize":"0.78em","fontWeight":"800","letterSpacing":"4px","marginBottom":"14px",
            }),
            html.Div([
                html.Span(t["price"], style={"color":"white","fontWeight":"900","fontSize":"2.4em","letterSpacing":"-1.5px"}),
                html.Span(t["period"], style={"color":"rgba(255,255,255,0.4)","fontSize":"0.9em","marginLeft":"6px","fontWeight":"600"}),
            ], style={"marginBottom":"4px"}),
            html.Div(t["seats"], style={
                "color":"rgba(255,255,255,0.55)","fontSize":"0.74em","fontWeight":"700",
                "letterSpacing":"1.5px","marginBottom":"10px","textTransform":"uppercase",
            }),
            html.Div(t["desc"], style={
                "color":"rgba(255,255,255,0.72)","fontSize":"0.88em","marginBottom":"22px","fontStyle":"italic",
            }),
            html.Div(style={"height":"1px","background":"rgba(255,255,255,0.08)","marginBottom":"22px"}),
            *[html.Div([
                html.Span("✓", style={"color":BULL,"fontWeight":"900","marginRight":"10px","flexShrink":"0"}),
                html.Span(f, style={"color":"rgba(255,255,255,0.85)","fontSize":"0.86em","lineHeight":"1.5"}),
            ], style={"display":"flex","alignItems":"flex-start","marginBottom":"10px"}) for f in t["features"]],
            html.A("Request a Call →", href="/book-call?source=enterprise", style={
                "display":"block","width":"100%","textAlign":"center","padding":"14px",
                "marginTop":"26px","borderRadius":"11px",
                "background":"linear-gradient(135deg,#A855F7,#9333EA)" if t["highlight"] else "transparent",
                "border":"2px solid " + (PURPLE if t["highlight"] else "rgba(168,85,247,0.4)"),
                "color":"white","fontWeight":"800","fontSize":"0.82em","letterSpacing":"2px",
                "textDecoration":"none","boxShadow":"0 8px 28px rgba(147,51,234,0.4)" if t["highlight"] else "none",
                "transition":"all 0.2s ease",
            }),
        ], className="reveal plan-card", style={
            "background":bg,"border":border,"borderRadius":"20px",
            "padding":"38px 30px","flex":"1","maxWidth":"340px",
            "boxShadow":glow,"position":"relative",
        })

    return html.Div([
        html.Div(className="hero-glow"),

        # ── Navbar ──────────────────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Span("BOJKET", style={
                    "background":"linear-gradient(135deg,#ffffff 0%,#A855F7 100%)",
                    "-webkit-background-clip":"text","-webkit-text-fill-color":"transparent","background-clip":"text",
                    "fontWeight":"900","fontSize":"1.3em","letterSpacing":"6px",
                }),
                html.Div("FOR TEAMS & INSTITUTIONS", style={
                    "color":PURPLE_LIGHT,"fontSize":"0.55em","letterSpacing":"3px","marginTop":"3px","fontWeight":"700",
                }),
            ]),
            html.Div([
                html.A("SOLO", href="/", style={
                    "color":"rgba(255,255,255,0.55)","fontSize":"0.72em","fontWeight":"700","letterSpacing":"2.5px",
                    "textDecoration":"none","marginRight":"20px",
                }),
                html.A("SIGN IN", href="/login", style={
                    "color":"rgba(255,255,255,0.75)","padding":"9px 22px","fontSize":"0.72em","fontWeight":"700",
                    "letterSpacing":"2.5px","textDecoration":"none","display":"inline-block",
                    "border":"1px solid rgba(255,255,255,0.18)","borderRadius":"8px",
                }),
            ], style={"display":"flex","alignItems":"center"}),
        ], style={"display":"flex","justifyContent":"space-between","alignItems":"center",
                  "padding":"22px 64px","borderBottom":"1px solid rgba(255,255,255,0.06)",
                  "position":"sticky","top":"0","backgroundColor":"rgba(6,6,8,0.92)",
                  "zIndex":"100","backdropFilter":"blur(20px)"}),

        # ── Hero ────────────────────────────────────────────────────────────
        html.Div([
            html.Div("FOR TEAMS", className="reveal", style={
                "color":PURPLE_LIGHT,"fontSize":"0.85em","fontWeight":"800",
                "letterSpacing":"5px","marginBottom":"26px",
            }),
            html.H1("Built for firms that trade seriously.", className="reveal", style={
                "color":"white","fontWeight":"900","fontSize":"3.6em","lineHeight":"1.08",
                "letterSpacing":"-2px","margin":"0 0 26px 0","maxWidth":"860px",
            }),
            html.Div("Multi-seat access. Admin controls. API integration. Direct line to the founder.",
                className="reveal", style={
                    "color":"rgba(255,255,255,0.65)","fontSize":"1.05em","fontWeight":"500",
                    "lineHeight":"1.7","maxWidth":"640px","marginBottom":"40px",
                }),
            html.A("Book a Private Call →", href="/book-call?source=enterprise", className="reveal cta-mega", style={
                "background":"linear-gradient(135deg,#A855F7,#9333EA)",
                "color":"white","padding":"20px 48px","borderRadius":"14px",
                "fontWeight":"800","fontSize":"1em","letterSpacing":"2px",
                "textDecoration":"none","display":"inline-block",
                "boxShadow":"0 12px 48px rgba(147,51,234,0.55), 0 0 0 1px rgba(168,85,247,0.7) inset",
            }),
        ], style={"padding":"80px 64px 56px 64px","maxWidth":"1200px","margin":"0 auto"}),

        # ── Trust strip (simple, 4 points) ──────────────────────────────────
        html.Div([
            html.Div([
                html.Div([
                    html.Div(icon, style={"fontSize":"1.4em","marginBottom":"10px"}),
                    html.Div(title, style={"color":"white","fontWeight":"800","fontSize":"0.88em","letterSpacing":"1.5px","marginBottom":"6px"}),
                    html.Div(desc, style={"color":"rgba(255,255,255,0.5)","fontSize":"0.78em","lineHeight":"1.6"}),
                ], style={"flex":"1","textAlign":"center"})
                for icon, title, desc in [
                    ("🔒", "Private & Secure", "Your signals stay yours."),
                    ("⚡", "Institutional-Grade", "10-factor engine, ML, backtesting."),
                    ("🛠", "Hands-On Support", "Direct line to the founder."),
                    ("📊", "Audit-Ready", "Full logs. CSV export."),
                ]
            ], className="reveal", style={"display":"flex","gap":"32px","maxWidth":"1100px","margin":"0 auto"}),
        ], style={"borderTop":"1px solid rgba(255,255,255,0.05)","borderBottom":"1px solid rgba(255,255,255,0.05)",
                  "padding":"44px 64px","backgroundColor":"rgba(147,51,234,0.03)"}),

        # ── Pricing ─────────────────────────────────────────────────────────
        html.Div([
            html.Div("PRICING", className="reveal", style={
                "color":PURPLE_LIGHT,"fontSize":"0.8em","fontWeight":"800","letterSpacing":"5px",
                "textAlign":"center","marginBottom":"16px",
            }),
            html.H2("Simple. Transparent. Real value.", className="reveal", style={
                "color":"white","fontWeight":"900","fontSize":"2.4em","textAlign":"center",
                "margin":"0 0 14px 0","letterSpacing":"-1.5px",
            }),
            html.Div("Every engagement starts with a private call. No surprises.",
                className="reveal", style={
                    "color":"rgba(255,255,255,0.5)","fontSize":"0.96em","textAlign":"center","marginBottom":"60px","fontStyle":"italic",
                }),
            html.Div([tier_card(t) for t in tiers],
                style={"display":"flex","gap":"24px","justifyContent":"center","flexWrap":"wrap","maxWidth":"1200px","margin":"0 auto"}),

            # White-label add-on banner
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("🎨  ", style={"fontSize":"1.3em","marginRight":"4px"}),
                        html.Span("WHITE LABEL AVAILABLE", style={
                            "color":PURPLE_LIGHT,"fontSize":"0.82em","fontWeight":"800","letterSpacing":"3px",
                        }),
                    ], style={"marginBottom":"10px","display":"flex","alignItems":"center","justifyContent":"center"}),
                    html.Div("Your logo. Your name. Your domain. Your brand.", style={
                        "color":"white","fontSize":"1.25em","fontWeight":"800","marginBottom":"10px","letterSpacing":"-0.5px",
                    }),
                    html.Div("White-labeling is an add-on to any tier. Pricing is customised to your firm, scope, and timeline.", style={
                        "color":"rgba(255,255,255,0.6)","fontSize":"0.9em","lineHeight":"1.65","maxWidth":"640px","margin":"0 auto",
                    }),
                ], style={"textAlign":"center"}),
            ], className="reveal", style={
                "maxWidth":"780px","margin":"56px auto 0 auto","padding":"32px 28px",
                "background":"linear-gradient(135deg, rgba(147,51,234,0.07), rgba(147,51,234,0.02))",
                "border":"1px solid rgba(147,51,234,0.3)","borderRadius":"18px",
            }),
        ], style={"padding":"92px 64px","backgroundColor":"#050507","borderTop":"1px solid rgba(255,255,255,0.04)"}),

        # ── What your firm gets (simplified to 6 cards, short copy) ────────
        html.Div([
            html.Div("WHAT YOUR FIRM GETS", className="reveal", style={
                "color":PURPLE_LIGHT,"fontSize":"0.8em","fontWeight":"800","letterSpacing":"5px",
                "textAlign":"center","marginBottom":"16px",
            }),
            html.H2("Everything your traders need.", className="reveal", style={
                "color":"white","fontWeight":"900","fontSize":"2.3em","textAlign":"center",
                "margin":"0 0 52px 0","letterSpacing":"-1.5px",
            }),
            html.Div([
                html.Div([
                    html.Div(icon, style={"fontSize":"2em","marginBottom":"14px"}),
                    html.Div(title, style={"color":"white","fontWeight":"800","fontSize":"1em","marginBottom":"8px","letterSpacing":"0.4px"}),
                    html.Div(desc, style={"color":"rgba(255,255,255,0.55)","fontSize":"0.86em","lineHeight":"1.65"}),
                ], className="reveal feature-card", style={
                    "background":"rgba(147,51,234,0.06)","border":"1px solid rgba(255,255,255,0.07)",
                    "borderRadius":"16px","padding":"26px","flex":"1","minWidth":"270px",
                })
                for icon, title, desc in [
                    ("👥", "Multi-Seat Admin", "One dashboard controls every trader. Add, remove, audit — in seconds."),
                    ("🔌", "REST API Access", "Pipe signals into your OMS, Slack, or internal tools."),
                    ("📈", "Per-Trader Analytics", "Every trader's win rate, streaks, and top assets — in one view."),
                    ("📑", "Audit Logs & Export", "Every signal, trade, and login. CSV-ready."),
                    ("🎯", "Signal Calibration", "Tune the engine to your firm's strategy. Weight factors. Set thresholds."),
                    ("🎨", "White Label Option", "Custom logo, name, colors, domain. Make it yours."),
                ]
            ], style={"display":"grid","gridTemplateColumns":"repeat(auto-fit, minmax(270px, 1fr))","gap":"20px","maxWidth":"1100px","margin":"0 auto"}),
        ], style={"padding":"92px 64px","borderTop":"1px solid rgba(255,255,255,0.04)"}),

        # ── Founder partnership — NEW section ──────────────────────────────
        html.Div([
            html.Div([
                html.Div("DIRECT FOUNDER ACCESS", className="reveal", style={
                    "color":PURPLE_LIGHT,"fontSize":"0.8em","fontWeight":"800","letterSpacing":"5px","marginBottom":"18px",
                }),
                html.H2("You're not talking to a support ticket.", className="reveal", style={
                    "color":"white","fontWeight":"900","fontSize":"2.3em","margin":"0 0 22px 0","letterSpacing":"-1.5px","lineHeight":"1.15",
                }),
                html.Div([
                    html.P("Every firm that joins Bojket gets a direct line to me — the founder. Not a chatbot. Not a junior CS rep. Me.", style={
                        "color":"rgba(255,255,255,0.78)","fontSize":"1.02em","lineHeight":"1.8","marginBottom":"14px",
                    }),
                    html.P("We stay in constant communication. Feature requests go straight to the roadmap. Bugs get my attention the same day. Your firm's edge becomes my job.", style={
                        "color":"rgba(255,255,255,0.62)","fontSize":"0.95em","lineHeight":"1.8","marginBottom":"14px",
                    }),
                    html.P("This isn't a SaaS subscription. It's a partnership — built on satisfaction, iteration, and real relationships.", style={
                        "color":"rgba(255,255,255,0.55)","fontSize":"0.92em","lineHeight":"1.8","fontStyle":"italic",
                    }),
                ], className="reveal"),
                html.Div([
                    *[html.Div([
                        html.Span("→  ", style={"color":PURPLE_LIGHT,"fontWeight":"900","marginRight":"4px"}),
                        html.Span(point, style={"color":"rgba(255,255,255,0.8)","fontSize":"0.9em","fontWeight":"600","letterSpacing":"0.3px"}),
                    ], style={"marginBottom":"10px"}) for point in [
                        "Dedicated WhatsApp / Signal / Discord channel with me",
                        "Monthly check-ins to review what's working",
                        "Feature requests built on your timeline",
                        "Zero-bureaucracy support — one message, one response",
                    ]],
                ], className="reveal", style={"marginTop":"30px"}),
            ], style={"maxWidth":"820px","margin":"0 auto"}),
        ], style={"padding":"92px 64px","borderTop":"1px solid rgba(255,255,255,0.04)",
                  "backgroundColor":"rgba(147,51,234,0.03)"}),

        # ── Who it's for ────────────────────────────────────────────────────
        html.Div([
            html.Div("WHO IT'S FOR", className="reveal", style={
                "color":PURPLE_LIGHT,"fontSize":"0.8em","fontWeight":"800","letterSpacing":"5px",
                "textAlign":"center","marginBottom":"16px",
            }),
            html.H2("Serious capital. Serious tools.", className="reveal", style={
                "color":"white","fontWeight":"900","fontSize":"2.3em","textAlign":"center",
                "margin":"0 0 52px 0","letterSpacing":"-1.5px",
            }),
            html.Div([
                html.Div([
                    html.Div(label, style={"color":PURPLE_LIGHT,"fontWeight":"800","fontSize":"0.72em","letterSpacing":"3px","marginBottom":"12px"}),
                    html.Div(title, style={"color":"white","fontWeight":"800","fontSize":"1.2em","marginBottom":"12px","lineHeight":"1.3"}),
                    html.Div(desc, style={"color":"rgba(255,255,255,0.6)","fontSize":"0.88em","lineHeight":"1.7"}),
                ], className="reveal", style={
                    "flex":"1","minWidth":"260px","padding":"30px 26px",
                    "background":"linear-gradient(180deg, rgba(147,51,234,0.04), transparent)",
                    "border":"1px solid rgba(147,51,234,0.18)","borderRadius":"16px",
                })
                for label, title, desc in [
                    ("PROP FIRMS", "Prop Trading Firms", "Give every trader an institutional edge. Track the desk. Scale without analysts."),
                    ("FAMILY OFFICES", "Family Offices", "Pro-grade intelligence without Bloomberg's price tag. Private. Yours."),
                    ("CRYPTO FUNDS", "Crypto Hedge Funds", "Built for 24/7 markets. ML learns your asset class. Backtested."),
                ]
            ], style={"display":"flex","gap":"22px","flexWrap":"wrap","maxWidth":"1100px","margin":"0 auto"}),
        ], style={"padding":"92px 64px","borderTop":"1px solid rgba(255,255,255,0.04)","backgroundColor":"rgba(147,51,234,0.02)"}),

        # ── Bottom CTA ──────────────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Div("THE NEXT STEP", className="reveal", style={
                    "color":PURPLE_LIGHT,"fontSize":"0.82em","fontWeight":"800","letterSpacing":"5px","marginBottom":"22px",
                }),
                html.H2("Talk to the founder.", className="reveal", style={
                    "color":"white","fontWeight":"900","fontSize":"3em","margin":"0 0 20px 0",
                    "letterSpacing":"-2px","lineHeight":"1.08",
                }),
                html.Div("One call. No sales deck. We figure out if Bojket fits your firm — together.",
                    className="reveal",
                    style={"color":"rgba(255,255,255,0.6)","fontSize":"1em","marginBottom":"40px","lineHeight":"1.75","fontStyle":"italic"}),
                html.A("Book a Private Call →", href="/book-call?source=enterprise", className="reveal cta-mega", style={
                    "background":"linear-gradient(135deg,#A855F7,#9333EA)",
                    "color":"white","padding":"22px 52px","borderRadius":"14px",
                    "fontWeight":"800","fontSize":"1.02em","letterSpacing":"2px",
                    "textDecoration":"none","display":"inline-block",
                    "boxShadow":"0 12px 48px rgba(147,51,234,0.55), 0 0 0 1px rgba(168,85,247,0.7) inset",
                }),
            ], style={"textAlign":"center"}),
        ], style={"padding":"110px 64px","borderTop":"1px solid rgba(255,255,255,0.05)"}),

        # ── Footer ──────────────────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Div("BOJKET", style={"color":"white","fontWeight":"900","fontSize":"1em","letterSpacing":"5px","marginBottom":"4px"}),
                html.Div("THE FUTURE OF TRADING.", style={"color":TEXT_MUTED,"fontSize":"0.68em","letterSpacing":"2px","fontWeight":"600"}),
            ], style={"flex":"1"}),
            html.Div([
                html.Span("📍", style={"fontSize":"0.9em","marginRight":"7px"}),
                html.Span("BASED IN VIENNA, AUSTRIA", style={"color":"white","fontWeight":"700","fontSize":"0.72em","letterSpacing":"2.5px"}),
            ], style={"flex":"1","display":"flex","alignItems":"center","justifyContent":"center"}),
            html.Div("© 2026 BOJKET  ·  NOT FINANCIAL ADVICE.", style={"color":TEXT_MUTED,"fontSize":"0.68em","letterSpacing":"2px","fontWeight":"600","flex":"1","textAlign":"right"}),
        ], style={"display":"flex","justifyContent":"space-between","alignItems":"center","padding":"32px 64px","borderTop":"1px solid rgba(255,255,255,0.05)"}),

    ], style={"backgroundColor":BG_DARK,"minHeight":"100vh","color":TEXT_MAIN,"position":"relative","overflow":"hidden"})


def _feature_card(icon,title,desc):
    return html.Div([
        html.Div(icon,style={"fontSize":"2em","marginBottom":"14px"}),
        html.Div(title,style={"color":"white","fontWeight":"700","fontSize":"0.98em","marginBottom":"8px"}),
        html.Div(desc,style={"color":"rgba(255,255,255,0.5)","fontSize":"0.84em","lineHeight":"1.65"}),
    ],className="feature-card",style={"backgroundColor":"rgba(147,51,234,0.06)","border":"1px solid rgba(255,255,255,0.07)","borderRadius":"16px","padding":"28px"})

def login_page():
    return html.Div([
        # ── Top bar ─────────────────────────────────────────────────────────
        html.Div([
            html.Span("←", id="lv-back", style={
                "color":"rgba(255,255,255,0.45)","cursor":"pointer","fontSize":"1.1em","marginRight":"14px",
            }),
            html.Span("BOJKET", id="lv-logo", style={
                "color":"white","fontWeight":"900","fontSize":"1.05em","letterSpacing":"6px","cursor":"pointer",
            }),
        ], style={"padding":"22px 48px","borderBottom":"1px solid rgba(255,255,255,0.06)",
                  "display":"flex","alignItems":"center"}),

        # ── Centered form ────────────────────────────────────────────────────
        html.Div([
            html.Div([
                # Small purple eyebrow
                html.Div("PRIVATE ACCESS", className="reveal", style={
                    "color":PURPLE_LIGHT,"fontSize":"0.78em","fontWeight":"800",
                    "letterSpacing":"5px","textAlign":"center","marginBottom":"20px",
                }),
                # Main heading
                html.H1("WELCOME BACK.", className="reveal", style={
                    "color":"white","fontWeight":"900","fontSize":"3em",
                    "letterSpacing":"-1.5px","textAlign":"center","margin":"0 0 14px 0",
                    "textTransform":"uppercase",
                }),
                html.Div("SIGN IN TO YOUR BOJKET ACCOUNT.", className="reveal", style={
                    "color":"rgba(255,255,255,0.45)","fontSize":"0.82em","fontWeight":"600",
                    "letterSpacing":"3px","textAlign":"center","marginBottom":"48px","textTransform":"uppercase",
                }),

                # Email
                html.Div("EMAIL", style={
                    "color":"rgba(255,255,255,0.7)","fontSize":"0.7em","fontWeight":"700",
                    "letterSpacing":"3px","marginBottom":"10px",
                }),
                dcc.Input(id="lv-email", type="email", placeholder="you@example.com",
                    className="inp", style={"marginBottom":"22px","textAlign":"center","letterSpacing":"1px"}),

                # Password
                html.Div("PASSWORD", style={
                    "color":"rgba(255,255,255,0.7)","fontSize":"0.7em","fontWeight":"700",
                    "letterSpacing":"3px","marginBottom":"10px",
                }),
                dcc.Input(id="lv-password", type="password", placeholder="••••••••",
                    className="inp", style={"marginBottom":"14px","textAlign":"center","letterSpacing":"2px"}),

                html.Div(id="lv-error", style={
                    "color":BEAR,"fontSize":"0.78em","marginBottom":"18px","minHeight":"22px",
                    "textAlign":"center","fontWeight":"600","letterSpacing":"1px",
                }),

                # Sign-in button
                html.Button("SIGN IN →", id="lv-submit", className="cta-mega", style={
                    "background":"linear-gradient(135deg,#A855F7,#9333EA)",
                    "color":"white","padding":"18px","fontSize":"0.92em","width":"100%",
                    "fontWeight":"800","letterSpacing":"3px","border":"none",
                    "borderRadius":"12px","cursor":"pointer","marginBottom":"32px",
                    "boxShadow":"0 10px 40px rgba(147,51,234,0.45), 0 0 0 1px rgba(168,85,247,0.6) inset",
                    "transition":"transform 0.2s ease, box-shadow 0.2s ease",
                }),

                # OR divider
                html.Div([
                    html.Div(style={"height":"1px","background":"rgba(255,255,255,0.08)","flex":"1"}),
                    html.Span("OR", style={"color":"rgba(255,255,255,0.3)","fontSize":"0.7em",
                             "padding":"0 16px","flexShrink":"0","letterSpacing":"3px","fontWeight":"700"}),
                    html.Div(style={"height":"1px","background":"rgba(255,255,255,0.08)","flex":"1"}),
                ], style={"display":"flex","alignItems":"center","marginBottom":"24px"}),

                # No account yet — book a call
                html.Div("NO ACCOUNT YET?", style={
                    "color":"rgba(255,255,255,0.5)","fontSize":"0.72em","fontWeight":"700",
                    "letterSpacing":"3px","textAlign":"center","marginBottom":"14px",
                }),
                html.A("BOOK A PRIVATE CALL →", href="/book-call", style={
                    "display":"block","width":"100%","padding":"16px",
                    "textAlign":"center","border":f"2px solid {PURPLE}",
                    "borderRadius":"12px","color":"white",
                    "fontWeight":"800","fontSize":"0.85em","letterSpacing":"3px",
                    "textDecoration":"none","textTransform":"uppercase",
                    "background":"rgba(147,51,234,0.08)",
                    "boxShadow":"0 0 28px rgba(147,51,234,0.2)",
                    "transition":"all 0.25s ease",
                }),
            ], className="reveal", style={"width":"100%","maxWidth":"440px"}),
        ], style={"display":"flex","justifyContent":"center","alignItems":"center",
                  "minHeight":"calc(100vh - 70px)","padding":"60px 24px"}),
    ], style={"backgroundColor":BG_DARK,"minHeight":"100vh","color":TEXT_MAIN})

def email_sent_page(email):
    return html.Div([html.Div([
        html.Div("✉️",style={"fontSize":"3.5em","marginBottom":"20px"}),
        html.Div("Check your inbox.",style={"color":"white","fontWeight":"800","fontSize":"2em","marginBottom":"10px","letterSpacing":"-1px"}),
        html.Div("We sent a confirmation link to",style={"color":"rgba(255,255,255,0.5)","fontSize":"0.95em","marginBottom":"6px"}),
        html.Div(email,style={"color":PURPLE_LIGHT,"fontWeight":"700","fontSize":"1em","marginBottom":"28px"}),
        html.Div([
            html.Span("Didn't receive it? ",style={"color":TEXT_MUTED,"fontSize":"0.82em"}),
            html.Span("Skip verification (demo mode)",id="skip-verify-btn",n_clicks=0,style={"color":PURPLE_LIGHT,"fontSize":"0.82em","cursor":"pointer","fontWeight":"600"}),
        ]),
    ],style={"textAlign":"center","maxWidth":"500px"})],
    style={"display":"flex","justifyContent":"center","alignItems":"center","minHeight":"100vh","backgroundColor":BG_DARK,"color":TEXT_MAIN})

ONBOARDING_QUESTIONS = [
    {"q":"How would you describe your trading experience?","answers":[("A","Complete beginner — just getting started"),("B","Intermediate — I know the basics"),("C","Experienced — I've been trading for years")],"response":"Bojket is built for every level — whether you're placing your first trade or your thousandth. The engine handles the heavy analysis so you can focus on the decision."},
    {"q":"What is your main goal with trading?","answers":[("A","Build a side income part-time"),("B","Trade full-time as my main income"),("C","Grow my savings long-term")],"response":"Bojket is designed to be your personal trading assistant at all times — helping you make high-probability decisions and stay disciplined, whatever your goal is."},
    {"q":"What matters most to you when entering a trade?","answers":[("A","Clear entry and exit levels — I want structure"),("B","High confidence signals — best setups only"),("C","Understanding why — I want to learn as I trade")],"response":"Bojket gives you all three — precise TP & SL levels, a confidence score for every signal, and a full breakdown of exactly why the engine fired."},
]

def onboarding_page(step=0,answers=None):
    if answers is None: answers=[]
    total=len(ONBOARDING_QUESTIONS)
    if step>=total:
        return html.Div([html.Div([
            html.Div("✦",style={"color":PURPLE_LIGHT,"fontSize":"2.8em","marginBottom":"18px"}),
            html.Div("You're all set.",style={"color":"white","fontWeight":"800","fontSize":"2.2em","marginBottom":"10px","letterSpacing":"-1px"}),
            html.Div("Bojket is ready to trade alongside you.",style={"color":"rgba(255,255,255,0.5)","fontSize":"0.95em","marginBottom":"36px"}),
            html.Button("Choose Your Plan →",id="ob-done-btn",n_clicks=0,className="cta-primary",style={"padding":"15px 36px","fontSize":"0.95em"}),
        ],style={"textAlign":"center","maxWidth":"480px"})],style={"display":"flex","justifyContent":"center","alignItems":"center","minHeight":"100vh","backgroundColor":BG_DARK})
    q=ONBOARDING_QUESTIONS[step]; prev_response=ONBOARDING_QUESTIONS[step-1]["response"] if step>0 else None
    return html.Div([
        html.Div([html.Div(style={"width":f"{(step/total)*100}%","backgroundColor":PURPLE,"height":"3px","borderRadius":"3px","transition":"width 0.4s"})],style={"backgroundColor":"#1e1a2e","height":"3px","width":"100%","position":"fixed","top":"0","left":"0","zIndex":"200"}),
        html.Div([html.Div([
            html.Div("BOJKET",style={"color":PURPLE_LIGHT,"fontWeight":"900","fontSize":"1.1em","letterSpacing":"4px","marginBottom":"44px","textAlign":"center"}),
            *([html.Div([html.Span("✦ ",style={"color":PURPLE_LIGHT}),html.Span(prev_response,style={"color":"rgba(255,255,255,0.65)","fontSize":"0.88em","lineHeight":"1.65","fontStyle":"italic"})],style={"background":"rgba(147,51,234,0.08)","border":"1px solid rgba(147,51,234,0.2)","borderRadius":"12px","padding":"16px 18px","marginBottom":"32px","maxWidth":"500px"},className="fade-in")] if prev_response else []),
            html.Div(f"Question {step+1} of {total}",style={"color":TEXT_MUTED,"fontSize":"0.7em","letterSpacing":"1.5px","fontWeight":"600","marginBottom":"14px","textAlign":"center","textTransform":"uppercase"}),
            html.Div(q["q"],style={"color":"white","fontWeight":"700","fontSize":"1.4em","marginBottom":"28px","textAlign":"center","maxWidth":"500px","lineHeight":"1.35","letterSpacing":"-0.5px"}),
            html.Div([html.Button([html.Span(letter,style={"color":PURPLE_LIGHT,"fontWeight":"800","fontSize":"0.8em","marginRight":"14px","border":f"1px solid {PURPLE_LIGHT}","borderRadius":"5px","padding":"2px 8px","flexShrink":"0"}),html.Span(text,style={"color":"rgba(255,255,255,0.75)","fontSize":"0.9em"})],id={"type":"ob-answer","index":i},n_clicks=0,className="ob-btn",style={"background":"rgba(255,255,255,0.03)","border":"1px solid rgba(255,255,255,0.1)","borderRadius":"12px","padding":"16px 20px","marginBottom":"12px","cursor":"pointer","width":"100%","display":"flex","alignItems":"center","textAlign":"left"}) for i,(letter,text) in enumerate(q["answers"])],style={"width":"100%","maxWidth":"500px"}),
        ],style={"display":"flex","flexDirection":"column","alignItems":"center","width":"100%","maxWidth":"580px"})],style={"display":"flex","justifyContent":"center","alignItems":"center","minHeight":"100vh","padding":"40px 20px","backgroundColor":BG_DARK}),
    ])

def pricing_page(billing="monthly"):
    is_annual = billing == "annual"

    # ── Prices & savings ──────────────────────────────────────────────────────
    hustler_price   = "€290"   if is_annual else "€29.99"
    veteran_price   = "€500"   if is_annual else "€49.99"
    hustler_orig    = "€359.88"   # 29.99 × 12  (crossed out in annual mode)
    veteran_orig    = "€599.88"   # 49.99 × 12

    # ── Billing toggle ────────────────────────────────────────────────────────
    mo_tab = dcc.Link("MONTHLY", href="/pricing", style={
        "backgroundColor": PURPLE if not is_annual else "transparent",
        "border": f"1px solid {PURPLE if not is_annual else 'rgba(255,255,255,0.15)'}",
        "color": "white" if not is_annual else "rgba(255,255,255,0.4)",
        "padding": "12px 32px", "borderRadius": "12px 0 0 12px",
        "fontSize": "1.02em", "cursor": "pointer",
        "fontWeight": "700" if not is_annual else "500",
        "letterSpacing": "1px",
        "textDecoration": "none", "display": "inline-flex", "alignItems": "center",
    })
    yr_tab = dcc.Link([
        html.Span("ANNUAL", style={"marginRight": "10px", "letterSpacing": "1px"}),
        html.Span("SAVE UP TO €100", style={
            "fontSize": "0.72em", "fontWeight": "800", "letterSpacing": "0.5px",
            "backgroundColor": f"{BULL}30", "color": BULL,
            "border": f"1px solid {BULL}70", "borderRadius": "5px",
            "padding": "3px 10px",
            "boxShadow": f"0 0 8px {BULL}40",
        }),
    ], href="/pricing?billing=annual", style={
        "backgroundColor": PURPLE if is_annual else "rgba(147,51,234,0.08)",
        "border": f"2px solid {PURPLE if is_annual else 'rgba(147,51,234,0.4)'}",
        "color": "white" if is_annual else "rgba(255,255,255,0.65)",
        "padding": "12px 26px", "borderRadius": "0 12px 12px 0",
        "fontSize": "1.02em",
        "cursor": "pointer", "fontWeight": "700" if is_annual else "600",
        "textDecoration": "none", "display": "inline-flex", "alignItems": "center", "gap": "0",
        "boxShadow": f"0 0 30px rgba(147,51,234,0.55)" if is_annual else "0 0 16px rgba(147,51,234,0.25)",
    })

    # (timer removed — no urgency banner)

    # ── Price block builders ──────────────────────────────────────────────────
    def price_block_annual(orig, price, save_label):
        return html.Div([
            html.Div([
                html.Span("was ", style={"color":"rgba(255,255,255,0.38)","fontSize":"0.74em","marginRight":"5px"}),
                html.Span(orig + "/yr", style={
                    "textDecoration": "line-through",
                    "textDecorationColor": "#f87171",
                    "textDecorationThickness": "2px",
                    "color": "rgba(248,113,113,0.65)",
                    "fontSize": "0.9em", "fontWeight": "600",
                }),
            ], style={"marginBottom": "5px"}),
            html.Div(price, style={
                "color": "white", "fontWeight": "900", "fontSize": "3.1em",
                "letterSpacing": "-1.5px", "lineHeight": "1",
            }),
            html.Div([
                html.Span("/year  ", style={"color": TEXT_MUTED, "fontSize": "0.76em"}),
                html.Span(f"✓  Save {save_label}", style={
                    "color": BULL, "fontSize": "0.68em", "fontWeight": "800",
                    "backgroundColor": f"{BULL}18", "border": f"1px solid {BULL}45",
                    "borderRadius": "5px", "padding": "2px 8px",
                }),
            ], style={"marginTop": "7px", "marginBottom": "28px", "display": "flex", "alignItems": "center", "gap": "6px"}),
        ])

    def price_block_monthly(price, sub):
        return html.Div([
            html.Div(price, style={"color":"white","fontWeight":"900","fontSize":"2.8em","marginBottom":"4px","letterSpacing":"-1px"}),
            html.Div(sub,   style={"color":TEXT_MUTED,"fontSize":"0.75em","marginBottom":"28px"}),
        ])

    # ── Card styles ───────────────────────────────────────────────────────────
    hustler_style = {
        "background": "#0a0910",
        "border": "1px solid rgba(255,255,255,0.05)",
        "borderRadius": "18px", "padding": "32px", "flex": "1", "maxWidth": "360px",
        "opacity": "0.8",
    }
    veteran_style = {
        "background": "linear-gradient(135deg,#12102a,#1a1238)",
        "border": f"2px solid {PURPLE}",
        "borderRadius": "18px", "padding": "32px", "flex": "1", "maxWidth": "360px",
        "boxShadow": f"0 0 {'60px rgba(147,51,234,0.35)' if is_annual else '50px rgba(147,51,234,0.2)'}",
    }

    return html.Div([
        html.Div([
            html.A("← Sign In", href="/login", style={
                "color":"rgba(255,255,255,0.5)","fontSize":"0.82em","fontWeight":"600",
                "textDecoration":"none","letterSpacing":"0.3px",
                "transition":"color 0.15s",
            }),
            html.Div("BOJKET", style={"color":PURPLE_LIGHT,"fontWeight":"900","fontSize":"1.1em","letterSpacing":"4px","textAlign":"center"}),
            html.Div(style={"width":"80px"}),  # spacer to keep BOJKET centred
        ], style={"padding":"22px 48px","borderBottom":"1px solid rgba(255,255,255,0.06)",
                  "display":"flex","justifyContent":"space-between","alignItems":"center"}),

        html.Div([
            html.Div("Simple pricing.", style={"color":"white","fontWeight":"800","fontSize":"2.8em","textAlign":"center","marginBottom":"10px","letterSpacing":"-1px"}),
            html.Div("Professional tools for serious traders. Choose your plan.", style={"color":"rgba(255,255,255,0.65)","fontSize":"0.98em","textAlign":"center","marginBottom":"28px"}),

            # ── Billing toggle ──────────────────────────────────────────────
            html.Div([mo_tab, yr_tab], style={"display":"flex","justifyContent":"center","marginBottom":"22px"}),

            # ── Plan cards ─────────────────────────────────────────────────
            html.Div([
                # Hustler
                html.Div([
                    html.Div("SIMPLE", style={"color":TEXT_MUTED,"fontSize":"0.64em","fontWeight":"500","letterSpacing":"2.5px","marginBottom":"14px"}),
                    price_block_annual(hustler_orig, hustler_price, "~€70") if is_annual else price_block_monthly(hustler_price, "per month"),
                    html.Div(style={"height":"1px","backgroundColor":"rgba(255,255,255,0.06)","marginBottom":"22px"}),
                    *[_plan_feature(t,c) for t,c in [
                        ("Real-time BUY/SELL/WAIT signals",True),("Up to 4 pattern indicators",True),
                        ("TP & SL auto-calculation",True),("Trade journal & streak tracker",True),
                        ("Price alerts",True),("Global market news",True),
                        ("7 Bojket AI messages / day (resets 24h)",True),("ML model (AI Lab)",True),
                        ("Backtesting engine",True),("Higher timeframe analysis",False),
                        ("RSI divergence detection",False),("Signal breakdown panel",False),
                    ]],
                    html.Button("Start with Simple →", id="buy-hustler-btn", n_clicks=0, style={
                        "backgroundColor": "transparent",
                        "border": f"1px solid {'rgba(52,211,153,0.5)' if is_annual else 'rgba(192,132,252,0.4)'}",
                        "color": BULL if is_annual else NEUTRAL,
                        "padding": "13px", "borderRadius": "10px", "fontSize": "0.88em",
                        "cursor": "pointer", "fontWeight": "600", "width": "100%", "marginTop": "28px",
                    }),
                ], className="plan-card", style=hustler_style),

                # Veteran
                html.Div([
                    html.Div([
                        html.Span("PREMIUM", style={"color":BULL,"fontSize":"0.64em","fontWeight":"800","letterSpacing":"2px"}),
                        html.Span("BEST VALUE", style={"color":"white","fontSize":"0.58em","background":PURPLE,"padding":"3px 10px","borderRadius":"20px","marginLeft":"10px","fontWeight":"700"}),
                        *([] if not is_annual else [
                            html.Span("🔥 ANNUAL DEAL", style={
                                "color": BULL, "fontSize": "0.55em", "fontWeight": "800",
                                "background": f"{BULL}22", "border": f"1px solid {BULL}55",
                                "padding": "2px 8px", "borderRadius": "20px", "marginLeft": "6px",
                            })
                        ]),
                    ], style={"marginBottom":"14px","display":"flex","alignItems":"center","flexWrap":"wrap","gap":"4px"}),
                    price_block_annual(veteran_orig, veteran_price, "~€100") if is_annual else html.Div([
                        html.Div([
                            html.Span("was ", style={"color":"rgba(255,255,255,0.38)","fontSize":"0.74em","marginRight":"5px"}),
                            html.Span("€79.99/mo", style={"textDecoration":"line-through","textDecorationColor":"#f87171","textDecorationThickness":"2px","color":"rgba(248,113,113,0.65)","fontSize":"0.9em","fontWeight":"600"}),
                        ], style={"marginBottom":"5px"}),
                        html.Div(veteran_price, style={"color":"white","fontWeight":"900","fontSize":"2.8em","marginBottom":"4px","letterSpacing":"-1px"}),
                        html.Div([
                            html.Span("per month  ", style={"color":TEXT_MUTED,"fontSize":"0.75em"}),
                            html.Span("✓  Save €30/mo", style={"color":BULL,"fontSize":"0.68em","fontWeight":"800","backgroundColor":f"{BULL}18","border":f"1px solid {BULL}45","borderRadius":"5px","padding":"2px 8px"}),
                        ], style={"marginBottom":"28px","display":"flex","alignItems":"center","gap":"6px"}),
                    ]),
                    html.Div(style={"height":"1px","backgroundColor":"rgba(255,255,255,0.08)","marginBottom":"22px"}),
                    *[_plan_feature(t,True) for t in [
                        "Everything in Hustler","All 8 pattern indicators",
                        "Higher timeframe bias analysis","RSI divergence detection",
                        "Full signal breakdown panel","Unlimited Bojket AI usage",
                        "XGBoost ML model + backtesting","Early access to new features",
                    ]],
                    html.Button("Go Premium →", id="buy-veteran-btn", n_clicks=0, className="cta-primary", style={
                        "padding": "13px", "fontSize": "0.88em", "width": "100%", "marginTop": "28px",
                    }),
                ], className="plan-card", style=veteran_style),
            ], style={"display":"flex","gap":"24px","justifyContent":"center","maxWidth":"800px","margin":"0 auto"}),

            html.Div(id="payment-msg", style={"color":TEXT_MUTED,"fontSize":"0.78em","textAlign":"center","marginTop":"24px","fontStyle":"italic"}),
            html.Div("🔒  Secure checkout  ·  Cancel anytime  ·  Not financial advice.", style={"color":"rgba(255,255,255,0.25)","fontSize":"0.72em","textAlign":"center","marginTop":"14px"}),
        ], style={"padding":"56px 24px","maxWidth":"920px","margin":"0 auto"}),
    ], style={"backgroundColor":BG_DARK,"minHeight":"100vh","color":TEXT_MAIN})

def _plan_feature(text,included):
    return html.Div([
        html.Span("✓  " if included else "✗  ", style={
            "color": BULL if included else "#f87171",
            "fontWeight": "700",
            "fontSize": "0.92em",
            "marginRight": "5px",
            "flexShrink": "0",
        }),
        html.Span(text, style={
            "color": "rgba(255,255,255,0.92)" if included else "rgba(255,255,255,0.55)",
            "fontSize": "0.92em",
            "lineHeight": "1.4",
        }),
    ], style={"marginBottom": "11px", "display": "flex", "alignItems": "flex-start"})


# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD DATA & SIGNAL ENGINE
# ══════════════════════════════════════════════════════════════════════════════


# =============================================================================
#  DASHBOARD UI HELPERS
# =============================================================================

# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD UI HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def make_toggles(active,max_pat=8):
    """Compact abbreviation chips — 3 columns, color-coded by sentiment, hover = full name."""
    chips=[]
    for pname,sentiment in ALL_PATTERNS:
        color=PAT_COLOR.get(sentiment,NEUTRAL); on=pname in active
        abbr=PAT_ABBR.get(pname,pname[:3].upper())
        chips.append(
            html.Span(abbr,
                id={"type":"pat-toggle","index":pname},
                n_clicks=0,
                title=pname,           # native hover tooltip → full name
                style={
                    "cursor":"pointer","userSelect":"none","display":"inline-flex",
                    "alignItems":"center","justifyContent":"center",
                    "width":"42px","height":"30px","margin":"3px",
                    "borderRadius":"6px","fontSize":"0.68em","fontWeight":"700",
                    "letterSpacing":"0.5px","transition":"all 0.12s ease",
                    "border":f"1px solid {color if on else '#2a2040'}",
                    "color":color if on else "#4a4468",
                    "backgroundColor":f"{color}22" if on else "transparent",
                    "boxShadow":f"0 0 6px {color}55" if on else "none",
                }
            )
        )
    return html.Div(chips,style={"display":"flex","flexWrap":"wrap","padding":"4px 0"})

def make_active_list(active):
    if not active:
        return [html.Div("None",style={"color":TEXT_MUTED,"fontSize":"0.7em","fontStyle":"italic","marginTop":"4px"})]
    sent_map={n:s for n,s in ALL_PATTERNS}
    items=[]
    for p in active:
        s=sent_map.get(p,"neutral"); color=PAT_COLOR.get(s,NEUTRAL)
        abbr=PAT_ABBR.get(p,p[:3].upper())
        items.append(html.Div([
            html.Span(abbr,title=p,style={"display":"inline-block","width":"34px","backgroundColor":f"{color}20",
                "border":f"1px solid {color}60","borderRadius":"4px","color":color,
                "fontSize":"0.62em","fontWeight":"700","textAlign":"center","padding":"1px 0","marginRight":"7px"}),
            html.Span(p,style={"color":TEXT_DIM,"fontSize":"0.68em","overflow":"hidden","textOverflow":"ellipsis","whiteSpace":"nowrap"}),
        ],style={"display":"flex","alignItems":"center","marginBottom":"5px","maxWidth":"150px"}))
    items.append(html.Div(f"{len(active)} / {MAX_IND}",
        style={"color":PURPLE,"fontSize":"0.6em","marginTop":"6px","fontWeight":"600","letterSpacing":"1px"}))
    return items

def lbl(text):
 return html.Div(text,style={"color":"rgba(168,85,247,0.7)","fontSize":"0.58em","fontWeight":"700","letterSpacing":"2px","textTransform":"uppercase","marginBottom":"4px"})
def tbtn(label,bid,active=False,tip=""):
    return dbc.Button(label,id=bid,color="dark",outline=True,title=tip,className="tool-btn",
        style={"border":f"1px solid {PURPLE if active else 'rgba(255,255,255,0.14)'}",
               "color":PURPLE_LIGHT if active else "rgba(255,255,255,0.78)",
               "background":"rgba(147,51,234,0.06)" if active else "rgba(255,255,255,0.02)",
               "padding":"5px 12px","fontSize":"0.85em","borderRadius":"7px","minWidth":"0",
               "transition":"all 0.18s ease","fontWeight":"600"})

TUTORIAL_CHIPS = [
    ("🎯 How do the signals work?",    "Explain how BUY, SELL and WAIT signals work on the dashboard, what the score means, and how to act on them."),
    ("🧠 What is the AI Lab?",          "Explain the AI Lab in simple terms — what ML training does, how it improves my signals, and what backtesting shows me."),
    ("🛠️ What tools do I have?",        "Give me a quick tour of all the tools in the dashboard — Patterns, Journal, News, Alerts, AI Lab — what each one does in one sentence."),
    ("📓 How do I use the journal?",    "Explain how the trade journal works, how trades get logged, and how it helps me improve over time."),
    ("⚡ Analyze the current signal", "Analyze the current signal on my screen right now. Tell me what the indicators are saying, whether it looks strong or weak, and what a disciplined trader would do."),
    ("🎯 Should I enter now?",        "Based on what's on my screen right now — the current signal, RSI, MACD, and price — should I consider entering a trade? Walk me through the reasoning, pros and cons."),
]

def _typing_bubble():
    """Three bouncing dots shown while AI is generating a response."""
    return html.Div([
        html.Span(className="typing-dot"),
        html.Span(className="typing-dot"),
        html.Span(className="typing-dot"),
    ], style={"padding":"12px 18px","borderRadius":"14px 14px 14px 3px","maxWidth":"80px",
              "backgroundColor":"#1a1a2e","alignSelf":"flex-start","display":"flex",
              "alignItems":"center","gap":"0"})

def render_chat_messages(messages):
    if not messages:
        chips = html.Div([
            html.Div("Quick questions — tap to ask:",style={"color":TEXT_MUTED,"fontSize":"0.68em","marginBottom":"6px","fontStyle":"italic"}),
            *[html.Button(label,id={"type":"quick-chip","index":msg},n_clicks=0,style={
                "backgroundColor":"transparent","border":f"1px solid {PURPLE}50","color":PURPLE_LIGHT,
                "borderRadius":"20px","padding":"4px 12px","fontSize":"0.68em","cursor":"pointer",
                "margin":"2px 3px 2px 0","display":"inline-block"})
              for label,msg in TUTORIAL_CHIPS],
        ],style={"marginTop":"10px"})
        return [
            html.Div([
                html.Div("✦",style={"color":PURPLE,"fontSize":"1.2em","marginBottom":"6px"}),
                html.Div("Hey — I'm Bojket, your AI trading co-pilot.",style={"color":TEXT_MAIN,"fontWeight":"700","fontSize":"0.85em","marginBottom":"5px"}),
                html.Div("I'll walk you through everything, help you read signals, understand the tools, and get the most out of every trade. Just ask.",style={"color":TEXT_DIM,"fontSize":"0.77em","lineHeight":"1.55","marginBottom":"2px"}),
                chips,
            ],style={"backgroundColor":f"{PURPLE}12","border":f"1px solid {PURPLE}25","borderRadius":"12px 12px 12px 3px","padding":"12px 14px","maxWidth":"96%"}),
        ]
    els = []
    last_i = len(messages) - 1
    for i, msg in enumerate(messages):
        is_user = msg["role"] == "user"
        is_last = i == last_i
        els.append(html.Div(
            msg["content"],
            className="fade-in" if is_last else "",
            style={"padding":"9px 13px",
                   "borderRadius":"14px 14px 3px 14px" if is_user else "14px 14px 14px 3px",
                   "maxWidth":"88%","fontSize":"0.8em","lineHeight":"1.55",
                   "alignSelf":"flex-end" if is_user else "flex-start",
                   "backgroundColor":PURPLE if is_user else "#1a1a2e",
                   "color":"white","wordBreak":"break-word","whiteSpace":"pre-wrap"}
        ))
    return els

def render_breakdown(reasons,signal,confidence):
    if not reasons: return html.Div("No data yet.",style={"color":TEXT_MUTED,"fontSize":"0.75em","fontStyle":"italic"})
    bar_color=BULL if signal=="BUY" else BEAR if signal=="SELL" else NEUTRAL
    items=[html.Div([html.Div([html.Span(f"{confidence}",style={"color":bar_color,"fontWeight":"700","fontSize":"1.4em"}),html.Span("/100",style={"color":TEXT_MUTED,"fontSize":"0.7em","marginLeft":"3px"})]),html.Div(html.Div(style={"width":f"{confidence}%","backgroundColor":bar_color,"height":"4px","borderRadius":"4px","transition":"width 0.4s"}),style={"backgroundColor":"#1e1a2e","borderRadius":"4px","height":"4px","marginTop":"6px","marginBottom":"14px"})])]
    for k,v in reasons.items():
        is_good=v.startswith("✅") or v.startswith("🔥"); is_warn=v.startswith("⚠️") or v.startswith("💤") or v.startswith("⚡")
        color=BULL if is_good else "#facc15" if is_warn else PURPLE_LIGHT if v.startswith("🧠") else TEXT_MUTED
        items.append(html.Div([html.Div(k,style={"color":TEXT_MUTED,"fontSize":"0.58em","fontWeight":"600","letterSpacing":"0.5px","marginBottom":"2px","textTransform":"uppercase"}),html.Div(v,style={"color":color,"fontSize":"0.72em","lineHeight":"1.3"})],style={"padding":"7px 0","borderBottom":f"1px solid {BORDER}33"}))
    return html.Div([html.Div("ENGINE ANALYSIS",style={"color":TEXT_MUTED,"fontSize":"0.58em","letterSpacing":"1.5px","fontWeight":"600","marginBottom":"10px"}),html.Div(items)])

def trade_entry_modal(signal,entry_price,default_tp,default_sl,atr):
    sig_color=BULL if signal=="BUY" else BEAR; sig_label="I Bought" if signal=="BUY" else "I Sold"
    return html.Div([html.Div([html.Div([
        html.Div(f"✅  {sig_label} — Set Trade Details",style={"color":sig_color,"fontWeight":"700","fontSize":"0.9em","marginBottom":"16px"}),
        html.Div([html.Div("Position Size",style={"color":TEXT_MUTED,"fontSize":"0.62em","letterSpacing":"1px","marginBottom":"4px","fontWeight":"500"}),html.Div([dcc.Input(id="pos-size-input",type="number",placeholder="e.g. 0.01",value="",className="inp",style={"flex":"1"}),html.Div("units",style={"color":TEXT_MUTED,"fontSize":"0.72em","marginLeft":"8px","alignSelf":"center","whiteSpace":"nowrap"})],style={"display":"flex","alignItems":"center"}),html.Div("How much? (BTC: 0.001, stocks: 10, etc.)",style={"color":TEXT_MUTED,"fontSize":"0.6em","marginTop":"3px","fontStyle":"italic"})],style={"marginBottom":"14px"}),
        html.Div([html.Div([html.Span("Take Profit 🎯",style={"color":TEXT_MUTED,"fontSize":"0.62em","letterSpacing":"1px","fontWeight":"500"}),html.Span(f"  ·  default: {default_tp}",style={"color":TEXT_MUTED,"fontSize":"0.58em","fontStyle":"italic"})],style={"marginBottom":"4px"}),dcc.Input(id="custom-tp-input",type="number",placeholder=str(default_tp),value="",className="inp")],style={"marginBottom":"14px"}),
        html.Div([html.Div([html.Span("Stop Loss 🛑",style={"color":TEXT_MUTED,"fontSize":"0.62em","letterSpacing":"1px","fontWeight":"500"}),html.Span(f"  ·  default: {default_sl}",style={"color":TEXT_MUTED,"fontSize":"0.58em","fontStyle":"italic"})],style={"marginBottom":"4px"}),dcc.Input(id="custom-sl-input",type="number",placeholder=str(default_sl),value="",className="inp")],style={"marginBottom":"18px"}),
        html.Div(f"ATR: {atr}  ·  Entry: {entry_price}",style={"color":TEXT_MUTED,"fontSize":"0.62em","marginBottom":"16px","fontStyle":"italic"}),
        html.Div([html.Button("Confirm Trade",id="confirm-trade-btn",n_clicks=0,style={"backgroundColor":f"{sig_color}15","border":f"1px solid {sig_color}50","color":sig_color,"padding":"8px 20px","borderRadius":"7px","fontSize":"0.8em","cursor":"pointer","fontWeight":"600","flex":"1"}),html.Div(style={"width":"8px"}),html.Button("Cancel",id="cancel-trade-btn",n_clicks=0,style={"backgroundColor":"transparent","border":f"1px solid {BORDER}","color":TEXT_MUTED,"padding":"8px 16px","borderRadius":"7px","fontSize":"0.8em","cursor":"pointer"})],style={"display":"flex","alignItems":"center"}),
    ],style={"backgroundColor":BG_CARD2,"border":f"1px solid {BORDER}","borderRadius":"12px","padding":"22px"})],style={"maxWidth":"420px","margin":"0 auto"})],
    style={"position":"fixed","top":"0","left":"0","width":"100%","height":"100%","backgroundColor":"rgba(0,0,0,0.75)","zIndex":"500","display":"flex","alignItems":"center","justifyContent":"center","padding":"20px"})

NEWS_PANEL_HIDDEN={"position":"fixed","top":"0","right":"0","width":"380px","height":"100vh","backgroundColor":"#06050f","borderLeft":f"1px solid {BORDER}","zIndex":"150","display":"none","boxShadow":"-8px 0 40px rgba(0,0,0,0.6)"}
NEWS_PANEL_SHOWN={**NEWS_PANEL_HIDDEN,"display":"block"}
BREAKDOWN_HIDDEN={"display":"none","width":"240px","flexShrink":"0","backgroundColor":BG_CARD,"borderLeft":f"1px solid {BORDER}","padding":"14px","overflowY":"auto","height":"640px"}
BREAKDOWN_SHOWN={**BREAKDOWN_HIDDEN,"display":"block"}
AILAB_PANEL_HIDDEN={"position":"fixed","top":"0","right":"0","width":"400px","height":"100vh","backgroundColor":"#06050f","borderLeft":f"1px solid {BORDER}","zIndex":"160","display":"none","boxShadow":"-8px 0 40px rgba(0,0,0,0.7)","overflowY":"auto"}
AILAB_PANEL_SHOWN={**AILAB_PANEL_HIDDEN,"display":"block"}
ADMIN_PANEL_HIDDEN={"position":"fixed","top":"0","left":"0","width":"720px","height":"100vh","backgroundColor":"#07060f","borderRight":f"1px solid {BORDER}","zIndex":"170","display":"none","boxShadow":"10px 0 60px rgba(0,0,0,0.8)","overflowY":"auto"}
ADMIN_PANEL_SHOWN={**ADMIN_PANEL_HIDDEN,"display":"block"}


# ── SHORT-TERM FORECAST ENGINE ────────────────────────────────────────────────

def compute_short_term_forecast(df, interval="5m"):
    """
    Predict the likely price direction and level over the next ~10 minutes.
    Combines linear regression, RSI, MACD histogram, recent momentum,
    volume confirmation, and Bollinger Band position.
    Returns a dict or None if not enough data.
    """
    if df is None or len(df) < 22:
        return None
    try:
        close  = df["close"].values.astype(float)
        last   = close[-1]

        signals = []   # +1 = bullish signal, -1 = bearish, 0 = neutral
        drivers = []   # human-readable reason strings

        # 1. Linear regression on last 20 candles — extrapolate 2 candles ahead
        x      = np.arange(20, dtype=float)
        y      = close[-20:]
        coeffs = np.polyfit(x, y, 1)           # slope, intercept
        slope  = coeffs[0]
        slope_pct = slope / last * 100
        lr_target = last + slope * 2            # extrapolated price

        if   slope_pct >  0.015: signals.append(1);  drivers.append(f"LR trend rising ({slope_pct:+.3f}%/candle)")
        elif slope_pct < -0.015: signals.append(-1); drivers.append(f"LR trend falling ({slope_pct:+.3f}%/candle)")
        else:                    signals.append(0);  drivers.append("LR trend flat")

        # 2. RSI momentum
        try:
            rsi_s  = ta.momentum.RSIIndicator(pd.Series(close), window=14).rsi()
            rsi_v  = rsi_s.iloc[-1]; rsi_p = rsi_s.iloc[-2]
            if   rsi_v < 30:                        signals.append(1);  drivers.append(f"RSI oversold ({rsi_v:.0f}) — bounce expected")
            elif rsi_v > 70:                        signals.append(-1); drivers.append(f"RSI overbought ({rsi_v:.0f}) — pullback risk")
            elif rsi_v > 55 and rsi_v > rsi_p:     signals.append(1);  drivers.append(f"RSI rising ({rsi_v:.0f})")
            elif rsi_v < 45 and rsi_v < rsi_p:     signals.append(-1); drivers.append(f"RSI falling ({rsi_v:.0f})")
            else:                                   signals.append(0)
        except: pass

        # 3. MACD histogram direction and expansion
        try:
            hist = ta.trend.MACD(pd.Series(close)).macd_diff().dropna()
            if len(hist) >= 2:
                h1, h0 = hist.iloc[-1], hist.iloc[-2]
                if   h1 > 0 and h1 > h0:  signals.append(1);  drivers.append("MACD histogram expanding bullish")
                elif h1 < 0 and h1 < h0:  signals.append(-1); drivers.append("MACD histogram expanding bearish")
                elif h1 > 0:              signals.append(1)
                elif h1 < 0:              signals.append(-1)
                else:                     signals.append(0)
        except: pass

        # 4. Recent 3-candle momentum
        if len(close) >= 4:
            rets     = [(close[-i] - close[-i-1]) / close[-i-1] for i in range(1, 4)]
            avg_ret  = float(np.mean(rets))
            if   avg_ret >  0.0002: signals.append(1);  drivers.append(f"Positive short momentum ({avg_ret*100:+.3f}%/candle)")
            elif avg_ret < -0.0002: signals.append(-1); drivers.append(f"Negative short momentum ({avg_ret*100:+.3f}%/candle)")
            else:                   signals.append(0)

        # 5. Volume confirmation
        if "volume" in df.columns:
            try:
                avg_vol   = df["volume"].iloc[-20:].mean()
                last_vol  = df["volume"].iloc[-1]
                vol_ratio = last_vol / avg_vol if avg_vol > 0 else 1.0
                last_dir  = 1 if close[-1] >= df["open"].iloc[-1] else -1
                if vol_ratio > 1.3:
                    signals.append(last_dir)
                    direction_word = "upward" if last_dir > 0 else "downward"
                    drivers.append(f"High volume confirms {direction_word} move ({vol_ratio:.1f}× avg)")
            except: pass

        # 6. Bollinger Band position
        try:
            bb       = ta.volatility.BollingerBands(pd.Series(close), window=20, window_dev=2)
            bb_up    = bb.bollinger_hband().iloc[-1]
            bb_lo    = bb.bollinger_lband().iloc[-1]
            bb_range = bb_up - bb_lo
            if bb_range > 0:
                bb_pct = (last - bb_lo) / bb_range
                if   bb_pct > 0.85: signals.append(-1); drivers.append("Near Bollinger upper — mean-reversion risk")
                elif bb_pct < 0.15: signals.append(1);  drivers.append("Near Bollinger lower — bounce opportunity")
                else:               signals.append(0)
        except: pass

        if not signals:
            return None

        net = sum(signals)
        n   = len(signals)

        # Confidence: how many signals agree, scaled to 35–92 range
        agreement = abs(net) / n                            # 0.0 – 1.0
        confidence = int(35 + agreement * 57)

        # ATR for price range
        try:
            atr = ta.volatility.AverageTrueRange(df["high"], df["low"], df["close"], window=14).average_true_range().iloc[-1]
        except:
            atr = last * 0.005

        # Price target: LR extrapolation nudged by net sentiment × ATR
        nudge = atr * 0.35 * (net / n)
        price_target = lr_target + nudge
        pct_change   = (price_target - last) / last * 100

        direction = "UP" if net > 0 else "DOWN" if net < 0 else "FLAT"

        return {
            "direction":  direction,
            "price":      round(price_target, 6),
            "low":        round(price_target - atr * 0.5, 6),
            "high":       round(price_target + atr * 0.5, 6),
            "pct_change": round(pct_change, 4),
            "confidence": confidence,
            "drivers":    drivers[:3],
        }
    except:
        return None


def render_forecast_card(forecast):
    """Render the 10-minute forecast as a styled card row."""
    if not forecast:
        return html.Div()

    direction = forecast["direction"]
    price     = forecast["price"]
    pct       = forecast["pct_change"]
    conf      = forecast["confidence"]
    drivers   = forecast["drivers"]
    low_est   = forecast["low"]
    high_est  = forecast["high"]

    dir_color = BULL if direction == "UP" else BEAR if direction == "DOWN" else NEUTRAL
    dir_arrow = "▲" if direction == "UP" else "▼" if direction == "DOWN" else "→"
    pct_str   = f"+{pct:.4f}%" if pct >= 0 else f"{pct:.4f}%"

    # Price formatted nicely
    if price >= 100:  price_fmt = f"{price:,.2f}"
    elif price >= 1:  price_fmt = f"{price:,.4f}"
    else:             price_fmt = f"{price:.6f}"

    if low_est >= 100:  lo_fmt, hi_fmt = f"{low_est:,.2f}", f"{high_est:,.2f}"
    elif low_est >= 1:  lo_fmt, hi_fmt = f"{low_est:,.4f}", f"{high_est:,.4f}"
    else:               lo_fmt, hi_fmt = f"{low_est:.6f}", f"{high_est:.6f}"

    return html.Div([
        # ── Title row ────────────────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Span("⏱  ", style={"color": dir_color, "fontSize":"1em"}),
                html.Span("~10-MIN FORECAST", style={"color":TEXT_MUTED,"fontSize":"0.72em","letterSpacing":"1.5px","fontWeight":"700"}),
            ], style={"display":"flex","alignItems":"center","flex":"1"}),
            html.Span("AI projection", style={"color":TEXT_MUTED,"fontSize":"0.68em","fontStyle":"italic","opacity":"0.65"}),
        ], style={"display":"flex","alignItems":"center","marginBottom":"10px"}),

        # ── Main figures row ─────────────────────────────────────────────────
        html.Div([
            # Direction + price
            html.Div([
                html.Span(dir_arrow, style={"color":dir_color,"fontWeight":"900","fontSize":"2.6em","lineHeight":"1","marginRight":"10px"}),
                html.Div([
                    html.Div(price_fmt, style={"color":TEXT_MAIN,"fontWeight":"700","fontSize":"1.4em","lineHeight":"1"}),
                    html.Div(pct_str,   style={"color":dir_color,"fontSize":"0.9em","fontWeight":"600","marginTop":"4px"}),
                ]),
            ], style={"display":"flex","alignItems":"center","flex":"1"}),

            # Confidence
            html.Div([
                html.Div([
                    html.Span("Confidence  ", style={"color":TEXT_MUTED,"fontSize":"0.75em"}),
                    html.Span(f"{conf}%", style={"color":dir_color,"fontSize":"0.78em","fontWeight":"700"}),
                ], style={"marginBottom":"5px","textAlign":"right"}),
                html.Div(
                    html.Div(style={"width":f"{conf}%","backgroundColor":dir_color,"height":"4px","borderRadius":"4px"}),
                    style={"backgroundColor":"#1e1a2e","borderRadius":"4px","height":"4px","width":"110px"}
                ),
                html.Div([
                    html.Span("Range: ", style={"color":TEXT_MUTED,"fontSize":"0.72em"}),
                    html.Span(f"{lo_fmt} – {hi_fmt}", style={"color":TEXT_DIM,"fontSize":"0.72em","fontWeight":"600"}),
                ], style={"marginTop":"5px","textAlign":"right"}),
            ], style={"textAlign":"right"}),
        ], style={"display":"flex","alignItems":"center","marginBottom":"12px"}),

        # ── Key drivers ──────────────────────────────────────────────────────
        *[html.Div([
            html.Span("·  ", style={"color":dir_color,"fontWeight":"700","fontSize":"0.76em"}),
            html.Span(d, style={"color":TEXT_DIM,"fontSize":"0.76em"}),
        ], style={"marginBottom":"3px"}) for d in drivers],

        # ── Disclaimer ───────────────────────────────────────────────────────
        html.Div([
            html.Span("⚠ ", style={"color":"#facc15","fontSize":"0.68em"}),
            html.Span(
                "Statistical projection only — markets are unpredictable. Combine this with your own read of the chart before acting.",
                style={"color":TEXT_MUTED,"fontSize":"0.66em","fontStyle":"italic","lineHeight":"1.5"}
            ),
        ], style={"marginTop":"10px","paddingTop":"8px","borderTop":f"1px solid {BORDER}"}),

    ], style={
        "backgroundColor": BG_CARD2,
       "border":         f"1px solid {BORDER}",
        "borderLeft":     f"3px solid {dir_color}",
        "borderRadius":   "10px",
        "padding":        "12px 16px",
        "marginBottom":   "7px",
    })


def build_admin_content():
    """Render list of customers who purchased the program."""
    from datetime import datetime, timedelta

    users = [u for u in REGISTERED_USERS.values() if u.get("plan") in ("hustler","veteran")]
    # Sort newest first by joined date
    try:
        users.sort(key=lambda u: u.get("last_login_iso",""), reverse=True)
    except Exception:
        pass

    now = datetime.now()
    active_count = 0
    for u in users:
        try:
            last = datetime.fromisoformat(u.get("last_login_iso",""))
            if (now - last) < timedelta(hours=24):
                active_count += 1
        except Exception:
            pass

    # ── stat cards ─────────────────────────────────────────────────────────
    def stat(num, label, color):
        return html.Div([
            html.Div(str(num), style={"color":color,"fontWeight":"800","fontSize":"2.4em","letterSpacing":"-1px","lineHeight":"1"}),
            html.Div(label, style={"color":TEXT_MUTED,"fontSize":"0.62em","letterSpacing":"2.5px","marginTop":"5px","fontWeight":"700"}),
        ], style={"backgroundColor":BG_CARD2,"border":f"1px solid {BORDER}","borderRadius":"12px",
                  "padding":"20px 24px","flex":"1","textAlign":"center"})

    stats_row = html.Div([
        stat(len(users), "TOTAL CUSTOMERS", TEXT_MAIN),
        stat(active_count, "ACTIVE (LAST 24H)", BULL),
        stat(len(users) - active_count, "INACTIVE", TEXT_MUTED),
    ], style={"display":"flex","gap":"10px","marginBottom":"28px"})

    # ── table header ───────────────────────────────────────────────────────
    tbl_header = html.Div([
        html.Div("",         style={"width":"16px","flexShrink":"0"}),
        html.Div("USERNAME", style={"color":TEXT_MUTED,"fontSize":"0.58em","fontWeight":"700","letterSpacing":"2px","flex":"1"}),
        html.Div("EMAIL",    style={"color":TEXT_MUTED,"fontSize":"0.58em","fontWeight":"700","letterSpacing":"2px","flex":"2"}),
        html.Div("DATE BOUGHT", style={"color":TEXT_MUTED,"fontSize":"0.58em","fontWeight":"700","letterSpacing":"2px","flex":"1.4"}),
        html.Div("LAST ACTIVE", style={"color":TEXT_MUTED,"fontSize":"0.58em","fontWeight":"700","letterSpacing":"2px","flex":"1.4"}),
        html.Div("RANK",     style={"color":TEXT_MUTED,"fontSize":"0.58em","fontWeight":"700","letterSpacing":"2px","flex":"1.2","textAlign":"right"}),
    ], style={"display":"flex","alignItems":"center","padding":"10px 18px",
              "borderBottom":f"1px solid {BORDER}","gap":"12px","marginBottom":"4px"})

    # ── rows ───────────────────────────────────────────────────────────────
    rows = []
    for u in users:
        is_active = False
        try:
            last = datetime.fromisoformat(u.get("last_login_iso",""))
            is_active = (now - last) < timedelta(hours=24)
        except Exception:
            pass
        dot = html.Div(style={
            "width":"9px","height":"9px","borderRadius":"50%","flexShrink":"0",
            "backgroundColor": BULL if is_active else "rgba(255,255,255,0.12)",
            "boxShadow": f"0 0 8px {BULL}" if is_active else "none",
        })
        rows.append(html.Div([
            dot,
            html.Div(u.get("username","—"), style={"color":TEXT_MAIN,"fontSize":"0.82em","fontWeight":"700","flex":"1","overflow":"hidden","textOverflow":"ellipsis","whiteSpace":"nowrap"}),
            html.Div(u.get("email","—"),    style={"color":TEXT_DIM,"fontSize":"0.76em","flex":"2","overflow":"hidden","textOverflow":"ellipsis","whiteSpace":"nowrap"}),
            html.Div(u.get("joined","—"),   style={"color":TEXT_MUTED,"fontSize":"0.72em","flex":"1.4"}),
            html.Div(u.get("last_login","—"),style={"color":BULL if is_active else TEXT_MUTED,"fontSize":"0.72em","flex":"1.4","fontWeight":"600" if is_active else "400"}),
            html.Div(
                render_rank_badge(get_rank(u.get("trades", [])), size="small"),
                style={"flex":"1.2","display":"flex","justifyContent":"flex-end"}
            ),
        ], style={"display":"flex","alignItems":"center","padding":"12px 18px",
                  "borderBottom":f"1px solid rgba(30,26,46,0.5)","gap":"12px"}))

    if not rows:
        body = html.Div("NO CUSTOMERS YET.", style={
            "color":TEXT_MUTED,"fontSize":"0.82em","fontStyle":"italic",
            "padding":"36px 18px","textAlign":"center","letterSpacing":"2px","fontWeight":"600",
        })
    else:
        body = html.Div([tbl_header] + rows)

    return html.Div([
        stats_row,
        html.Div(body, style={"backgroundColor":BG_CARD2,"border":f"1px solid {BORDER}",
                              "borderRadius":"12px","overflow":"hidden"}),
    ], style={"padding":"20px 22px 40px 22px"})


def build_admin_analytics():
    """Render per-user trading analytics in the admin panel."""
    users = list(REGISTERED_USERS.values())

    all_trades  = [t for u in users for t in u.get("trades", [])]
    total_trades = len(all_trades)
    sys_wins     = sum(1 for t in all_trades if "TP" in str(t.get("result","")))
    sys_wr       = f"{100*sys_wins//total_trades}%" if total_trades else "—"
    active_traders = len([u for u in users if u.get("trades")])
    most_active_u  = max(users, key=lambda u: len(u.get("trades",[])), default=None)
    most_active_name = most_active_u["username"] if most_active_u and most_active_u.get("trades") else "—"

    def stat(val, label, color):
        return html.Div([
            html.Div(str(val), style={"color":color,"fontWeight":"800","fontSize":"2.2em","letterSpacing":"-1px","lineHeight":"1"}),
            html.Div(label,    style={"color":TEXT_MUTED,"fontSize":"0.6em","letterSpacing":"2px","marginTop":"4px","fontWeight":"600"}),
        ], style={"backgroundColor":BG_CARD2,"border":f"1px solid {BORDER}","borderRadius":"10px","padding":"16px 20px","flex":"1","textAlign":"center"})

    stats_row = html.Div([
        stat(total_trades,    "TOTAL TRADES",    TEXT_MAIN),
        stat(sys_wr,          "SYSTEM WIN RATE", BULL),
        stat(active_traders,  "ACTIVE TRADERS",  NEUTRAL),
        stat(most_active_name,"MOST ACTIVE",     "#facc15"),
    ], style={"display":"flex","gap":"10px","marginBottom":"28px"})

    PLAN_COLORS  = {"hustler":"#facc15","veteran":BULL,"admin":PURPLE}
    PLAN_LABELS  = {"hustler":"Simple","veteran":"Premium","admin":"Admin"}
    COL_NAMES    = ["USER","PLAN","TRADES","WINS","LOSSES","WIN RATE","STREAK","TOP ASSET","LAST TRADE"]
    COL_WIDTHS   = ["1","0.9","0.7","0.6","0.7","0.8","0.7","1","1.3"]

    tbl_header = html.Div([
        html.Div(c, style={"color":TEXT_MUTED,"fontSize":"0.58em","fontWeight":"700","letterSpacing":"1.5px","flex":w})
        for c,w in zip(COL_NAMES, COL_WIDTHS)
    ], style={"display":"flex","padding":"8px 14px","borderBottom":f"1px solid {BORDER}","marginBottom":"4px"})

    rows = []
    for u in users:
        trades   = u.get("trades", [])
        total    = len(trades)
        wins     = sum(1 for t in trades if "TP" in str(t.get("result","")))
        losses   = sum(1 for t in trades if "SL" in str(t.get("result","")))
        wr_val   = (100*wins//total) if total else None
        wr_str   = f"{wr_val}%" if wr_val is not None else "—"
        wr_color = (BULL if wr_val >= 50 else BEAR) if wr_val is not None else TEXT_MUTED

        streak = 0
        for t in reversed(trades):
            if "TP" in str(t.get("result","")): streak += 1
            else: break
        streak_txt = (f"🔥 {streak}" if streak >= 2 else (f"✅ {streak}" if streak == 1 else "—"))

        top_asset_c = Counter(t.get("symbol","") for t in trades if t.get("symbol"))
        top_asset   = top_asset_c.most_common(1)[0][0] if top_asset_c else "—"

        plan_color = PLAN_COLORS.get(u.get("plan",""), TEXT_MUTED)
        plan_label = PLAN_LABELS.get(u.get("plan",""), "—")

        rows.append(html.Div([
            html.Div(u.get("username","—"),  style={"color":TEXT_MAIN,"fontSize":"0.78em","fontWeight":"600","flex":"1","overflow":"hidden","textOverflow":"ellipsis","whiteSpace":"nowrap"}),
            html.Div(html.Span(plan_label,   style={"backgroundColor":f"{plan_color}18","border":f"1px solid {plan_color}40","color":plan_color,"borderRadius":"20px","padding":"2px 8px","fontSize":"0.64em","fontWeight":"700"}), style={"flex":"0.9"}),
            html.Div(str(total) if total else "—",   style={"color":TEXT_DIM,"fontSize":"0.78em","flex":"0.7"}),
            html.Div(str(wins)  if total else "—",   style={"color":BULL,    "fontSize":"0.78em","flex":"0.6","fontWeight":"600" if wins   else "400"}),
            html.Div(str(losses)if total else "—",   style={"color":BEAR,    "fontSize":"0.78em","flex":"0.7","fontWeight":"600" if losses else "400"}),
            html.Div(wr_str,                         style={"color":wr_color, "fontSize":"0.78em","flex":"0.8","fontWeight":"700"}),
            html.Div(streak_txt,                     style={"color":BULL if streak else TEXT_MUTED,"fontSize":"0.75em","flex":"0.7"}),
            html.Div(top_asset,                      style={"color":NEUTRAL,  "fontSize":"0.75em","flex":"1"}),
            html.Div(u.get("last_trade","—"),         style={"color":TEXT_MUTED,"fontSize":"0.68em","flex":"1.3"}),
        ], style={"display":"flex","alignItems":"center","padding":"10px 14px","borderBottom":f"1px solid rgba(30,26,46,0.5)","gap":"8px"}))

    if not rows:
        table_body = html.Div("No users registered yet.",
            style={"color":TEXT_MUTED,"fontSize":"0.78em","fontStyle":"italic","padding":"14px"})
    else:
        table_body = html.Div([tbl_header]+rows,
            style={"backgroundColor":BG_CARD2,"border":f"1px solid {BORDER}","borderRadius":"12px","overflow":"hidden"})

    return html.Div([
        stats_row,
        html.Div("PER-USER TRADING ANALYTICS", style={"color":TEXT_MUTED,"fontSize":"0.6em","letterSpacing":"2px","fontWeight":"700","marginBottom":"12px"}),
        table_body,
    ], style={"padding":"20px 22px 40px 22px"})


def dashboard_page(plan="admin"):
    limits=PLAN_LIMITS.get(plan,PLAN_LIMITS[None])
    plan_badge_color=BULL if plan in ["admin","veteran"] else "#facc15"
    plan_label={"admin":"Admin","veteran":"Profitable Veteran","hustler":"Hustler"}.get(plan,"Hustler")

    return html.Div([
# ── TOPBAR ─────────────────────────────────────────────────────────
        html.Div([
            # Left — logo block
            html.Div([
                html.Span("BOJKET", style={
                    "background":"linear-gradient(135deg,#ffffff 0%,#A855F7 100%)",
                    "-webkit-background-clip":"text","-webkit-text-fill-color":"transparent","background-clip":"text",
                    "fontWeight":"900","fontSize":"1.1em","letterSpacing":"5px",
                    "filter":"drop-shadow(0 0 14px rgba(168,85,247,0.25))",
                }),
                html.Div("The future of trading.", style={
                    "color":"rgba(168,85,247,0.7)","fontSize":"0.52em","letterSpacing":"2.5px",
                    "marginTop":"2px","fontWeight":"600","textTransform":"uppercase",
                }),
            ], style={"minWidth":"150px"}),

            # Middle — tool row
            html.Div([
                tbtn("☰","market-btn",tip="Browse all markets"),
                html.Div(style={"width":"6px"}),
                dcc.Dropdown(id="symbol-input", options=ALL_OPTIONS, value="BTC-USD",
                    searchable=True, clearable=False, placeholder="Search...",
                    style={"width":"170px","backgroundColor":BG_CARD,"color":"black",
                           "border":f"1px solid {BORDER}","borderRadius":"7px","fontSize":"0.82em"}),
                html.Div(style={"width":"5px"}),
                dcc.Dropdown(id="interval-dropdown",
                    options=[{"label":l,"value":v} for l,v in [("1m","1m"),("5m","5m"),("15m","15m"),("30m","30m"),("1h","1h"),("2h","2h"),("3h","3h"),("4h","4h"),("1D","1d")]],
                    value="5m", clearable=False,
                    style={"width":"72px","backgroundColor":BG_CARD,"color":"black",
                           "border":f"1px solid {BORDER}","borderRadius":"7px","fontSize":"0.82em"}),

                # Divider
                html.Div(style={"width":"1px","height":"22px",
                    "background":"linear-gradient(180deg, transparent, rgba(147,51,234,0.35), transparent)",
                    "margin":"0 12px","flexShrink":"0"}),

                tbtn("📓","journal-btn",tip="Trade Journal — log & review your trades"),
                html.Div(style={"width":"4px"}),
            

                # Bell with dropdown
                html.Div([
                    html.Button("🔔", id="alert-btn", n_clicks=0, title="Notifications",
                        className="topbar-icon-btn",
                        style={"border":"1px solid rgba(255,255,255,0.14)","color":"rgba(255,255,255,0.75)",
                               "backgroundColor":"rgba(255,255,255,0.02)","padding":"5px 11px","fontSize":"0.85em",
                               "borderRadius":"7px","cursor":"pointer","minWidth":"0",
                               "transition":"all 0.18s ease"}),
                    html.Div([
                        html.Button([html.Span("🔔",style={"marginRight":"8px"}),"Set Price Alert"],
                            id="alert-dropdown-price-btn", n_clicks=0,
                            style={"display":"flex","alignItems":"center","width":"100%","background":"transparent",
                                   "border":"none","color":"rgba(255,255,255,0.85)","padding":"9px 13px",
                                   "fontSize":"0.8em","borderRadius":"7px","cursor":"pointer","textAlign":"left",
                                   "fontWeight":"500","whiteSpace":"nowrap"}),
                        html.Div(style={"height":"1px","backgroundColor":"rgba(255,255,255,0.07)","margin":"2px 6px"}),
                        html.Button([html.Span("🔕",style={"marginRight":"8px"}),"Mute Notifications"],
                            id="alert-dropdown-mute-btn", n_clicks=0,
                            style={"display":"flex","alignItems":"center","width":"100%","background":"transparent",
                                   "border":"none","color":"rgba(255,255,255,0.85)","padding":"9px 13px",
                                   "fontSize":"0.8em","borderRadius":"7px","cursor":"pointer","textAlign":"left",
                                   "fontWeight":"500","whiteSpace":"nowrap"}),
                    ], id="alert-dropdown",
                    style={"display":"none","position":"absolute","top":"calc(100% + 8px)","left":"0",
                           "backgroundColor":"#0f0e18","border":"1px solid rgba(255,255,255,0.14)",
                           "borderRadius":"10px","padding":"5px","minWidth":"188px","zIndex":"600",
                           "boxShadow":"0 8px 32px rgba(0,0,0,0.7)"}),
                ], style={"position":"relative"}),

                html.Div(style={"width":"4px"}),

                # Divider
                html.Div(style={"width":"1px","height":"22px",
                    "background":"linear-gradient(180deg, transparent, rgba(147,51,234,0.35), transparent)",
                    "margin":"0 12px","flexShrink":"0"}),

                tbtn("🧠  AI Lab","ailab-btn",tip="AI Lab — ML training, backtesting & insights"),
                html.Div(style={"width":"14px"}),
                html.Div(id="rank-badge-container", children=[render_rank_badge(RANKS[0])]),
                html.Div(style={"width":"4px"}),
            ], style={"display":"flex","alignItems":"center"}),

            # Right — plan badge + Discord + Sign out + Admin + Refresh
            html.Div([
                # Plan badge — gradient pill with glow
                html.Span(plan_label, style={
                    "background":f"linear-gradient(135deg,{plan_badge_color}18,{plan_badge_color}05)",
                    "color":plan_badge_color,"fontSize":"0.6em","fontWeight":"700",
                    "border":f"1px solid {plan_badge_color}55","padding":"5px 12px","borderRadius":"100px",
                    "marginRight":"14px","letterSpacing":"1.2px","textTransform":"uppercase",
                    "boxShadow":f"0 0 14px {plan_badge_color}25",
                }),

                # Discord
                html.A([
                    html.Img(src="https://cdn.simpleicons.org/discord/ffffff",
                        style={"width":"13px","height":"13px","marginRight":"6px","verticalAlign":"middle","opacity":"0.85"}),
                    html.Span("Discord", style={"verticalAlign":"middle","letterSpacing":"0.4px"}),
                ], href="https://discord.gg/e2merC6eFE", target="_blank",
                className="topbar-pill-btn discord",
                style={
                    "color":"rgba(255,255,255,0.8)","fontSize":"0.7em","fontWeight":"600",
                    "textDecoration":"none","display":"inline-flex","alignItems":"center",
                    "border":"1px solid rgba(88,101,242,0.45)","borderRadius":"7px",
                    "padding":"5px 12px","background":"linear-gradient(135deg,rgba(88,101,242,0.14),rgba(88,101,242,0.04))",
                    "marginRight":"10px","transition":"all 0.18s ease",
                }),

                # Sign Out
                html.A("✉  Support", href="mailto:contact@bojket.com", title="Email contact@bojket.com",
                    className="topbar-pill-btn",
                    style={"color":"rgba(255,255,255,0.65)","fontSize":"0.7em",
                           "marginRight":"10px","fontWeight":"600","padding":"5px 12px",
                           "border":"1px solid rgba(147,51,234,0.22)","borderRadius":"7px",
                           "background":"rgba(147,51,234,0.05)",
                           "textDecoration":"none","transition":"all 0.18s ease"}),
                html.Span("Sign Out", id="signout-btn", n_clicks=0, title="Log out of your account",
                    className="topbar-pill-btn",
                    style={"color":"rgba(255,255,255,0.55)","fontSize":"0.7em","cursor":"pointer",
                           "marginRight":"10px","fontWeight":"600","padding":"5px 12px",
                           "border":"1px solid rgba(255,255,255,0.08)","borderRadius":"7px",
                           "transition":"all 0.18s ease"}),

                # Admin
                dbc.Button("⚙  Admin", id="admin-btn", n_clicks=0, color="dark", outline=False,
                    title="Open Admin Panel",
                    style={"background":"linear-gradient(135deg,#A855F7,#9333EA)",
                           "border":"1px solid rgba(168,85,247,0.6)","color":"white",
                           "padding":"5px 14px","fontSize":"0.72em","borderRadius":"7px",
                           "marginRight":"8px","fontWeight":"700","letterSpacing":"1.5px",
                           "textTransform":"uppercase",
                           "boxShadow":"0 4px 18px rgba(147,51,234,0.38)",
                           "display":"inline-block" if plan=="admin" else "none"}),

                # Theme placeholder (hidden — kept so callbacks don't break)
                html.Div(id="theme-btn", style={"display":"none"}),

                # Refresh
                dbc.Button("↺", id="refresh-btn", color="dark", outline=True,
                    title="Refresh chart data now",
                    style={"border":"1px solid rgba(168,85,247,0.35)","color":PURPLE_LIGHT,
                           "padding":"5px 12px","fontSize":"0.92em","borderRadius":"7px",
                           "background":"rgba(147,51,234,0.06)",
                           "transition":"all 0.18s ease"}),
            ], style={"display":"flex","alignItems":"center"}),

        ], style={"display":"flex","alignItems":"center","justifyContent":"space-between",
                  "padding":"13px 26px","borderBottom":"1px solid rgba(147,51,234,0.15)",
                  "background":"linear-gradient(180deg, #0a0710 0%, #050508 100%)",
                  "position":"sticky","top":"0","zIndex":"100",
                  "boxShadow":"0 4px 24px rgba(0,0,0,0.4)"}),

        # ── PANEL AREA (market / journal / alert — NOT pattern, that's beside the chart) ──
        html.Div([
            html.Div(id="market-panel",style={"display":"none"},children=[html.Div([html.Div([html.Div(f"{CATEGORY_ICONS.get(cat,'')}  {cat.upper()}",style={"color":TEXT_MUTED,"fontSize":"0.58em","letterSpacing":"1.5px","marginBottom":"7px","fontWeight":"500"}),html.Div([html.Span(LABELS.get(s,s),id={"type":"sym-btn","index":s},n_clicks=0,className="sym-pill",style={"cursor":"pointer","display":"inline-block","color":TEXT_DIM,"fontSize":"0.76em","padding":"3px 12px","margin":"2px 3px 2px 0","borderRadius":"20px","border":f"1px solid {BORDER}","transition":"all 0.15s ease"}) for s in syms])],style={"marginBottom":"12px"}) for cat,syms in SYMBOLS.items()],style={"display":"flex","flexWrap":"wrap","gap":"0 28px"})]),
            html.Div(id="journal-panel",style={"display":"none"},children=[html.Div([html.Div(id="streak-display",style={"marginBottom":"8px"}),html.Div("TRADE JOURNAL",style={"color":PURPLE_LIGHT,"fontSize":"0.62em","letterSpacing":"3px","marginBottom":"12px","fontWeight":"800"}),html.Div(id="journal-table")])]),
        ],id="panel-area",style={"borderBottom":f"1px solid {BORDER}","backgroundColor":"#050508"}),

        # ── PRICE ALERT FLOATING CARD (near bell, top-right) ───────────────────
        html.Div([
            # Header
            html.Div([
                html.Div([
                    html.Span("🔔", style={"fontSize":"1.1em","marginRight":"9px"}),
                    html.Div([
                        html.Div("PRICE ALERT", style={"color":"white","fontWeight":"800","fontSize":"0.78em","letterSpacing":"2px"}),
                        html.Div("Get notified when price hits your target", style={"color":TEXT_MUTED,"fontSize":"0.62em","marginTop":"1px"}),
                    ]),
                ], style={"display":"flex","alignItems":"center","flex":"1"}),
                html.Button("✕", id="alert-close-btn", n_clicks=0, style={
                    "backgroundColor":"transparent","border":f"1px solid rgba(248,113,113,0.35)",
                    "color":"#f87171","padding":"3px 9px","borderRadius":"5px","fontSize":"0.8em","cursor":"pointer",
                }),
            ], style={"display":"flex","alignItems":"center","marginBottom":"18px"}),
            # Input row
            html.Div([
                dcc.Input(id="alert-input", type="number", placeholder="Enter target price...",
                    style={"backgroundColor":"#0a0910","border":f"1px solid rgba(147,51,234,0.4)",
                           "color":"white","padding":"10px 14px","borderRadius":"8px","fontSize":"0.85em",
                           "width":"100%","outline":"none","boxSizing":"border-box",
                           "boxShadow":"0 0 0 0px rgba(147,51,234,0)","transition":"box-shadow 0.2s"}),
            ], style={"marginBottom":"12px"}),
            # Buttons
            html.Div([
                html.Button("Set Alert", id="set-alert-btn", n_clicks=0, style={
                    "flex":"1","backgroundColor":PURPLE,"border":"none","color":"white",
                    "padding":"10px 0","borderRadius":"8px","fontSize":"0.82em","cursor":"pointer",
                    "fontWeight":"700","letterSpacing":"0.4px",
                    "boxShadow":"0 4px 16px rgba(147,51,234,0.4)",
                }),
                html.Button("Clear", id="clear-alert-btn", n_clicks=0, style={
                    "backgroundColor":"transparent","border":"1px solid rgba(255,255,255,0.12)",
                    "color":TEXT_MUTED,"padding":"10px 18px","borderRadius":"8px","fontSize":"0.82em","cursor":"pointer",
                }),
            ], style={"display":"flex","gap":"8px","marginBottom":"10px"}),
            # Status
            html.Div(id="alert-status", style={"fontSize":"0.74em","color":BULL,"minHeight":"16px","textAlign":"center","fontWeight":"600"}),
        ], id="alert-panel", style={
            "display":"none","position":"fixed","top":"62px","right":"230px",
            "width":"280px","backgroundColor":"#0d0c1a",
            "border":f"1px solid rgba(147,51,234,0.45)",
            "borderRadius":"14px","padding":"18px 20px","zIndex":"500",
            "boxShadow":"0 16px 48px rgba(0,0,0,0.75), 0 0 0 1px rgba(147,51,234,0.1)",
        }),

        # ── ADMIN PANEL (fixed overlay, z=170, left side) ───────────────────
        html.Div(id="admin-panel",style=ADMIN_PANEL_HIDDEN,children=[
            # Sticky header with tab switcher
            html.Div([
                html.Div([
                    html.Span("⚙",style={"fontSize":"1.1em","marginRight":"10px"}),
                    html.Div([
                        html.Div("ADMIN PANEL",style={"color":TEXT_MAIN,"fontWeight":"800","fontSize":"0.76em","letterSpacing":"3px"}),
                        html.Div("Bojket command center",style={"color":TEXT_MUTED,"fontSize":"0.58em","marginTop":"1px"}),
                    ]),
                ],style={"display":"flex","alignItems":"center","flex":"1"}),
                # Tab buttons
                html.Div([
                    html.Button("MEMBERS", id="admin-tab-members-btn", n_clicks=0,
                        style={"backgroundColor":f"{PURPLE}20","border":f"1px solid {PURPLE}50","color":NEUTRAL,
                               "padding":"4px 14px","borderRadius":"5px","fontSize":"0.65em","cursor":"pointer",
                               "fontWeight":"700","letterSpacing":"1px","marginRight":"6px"}),
                    html.Button("ANALYTICS", id="admin-tab-analytics-btn", n_clicks=0,
                        style={"backgroundColor":"transparent","border":f"1px solid {BORDER}","color":TEXT_MUTED,
                               "padding":"4px 14px","borderRadius":"5px","fontSize":"0.65em","cursor":"pointer",
                               "fontWeight":"700","letterSpacing":"1px","marginRight":"12px"}),
                ],style={"display":"flex","alignItems":"center"}),
                html.Button("✕",id="admin-close-btn",n_clicks=0,
                            style={"backgroundColor":"transparent","border":f"1px solid {BEAR}40","color":BEAR,"padding":"4px 10px","borderRadius":"5px","fontSize":"0.8em","cursor":"pointer"}),
            ],style={"display":"flex","alignItems":"center","padding":"14px 18px","borderBottom":f"1px solid {BORDER}",
                     "backgroundColor":"#0a0818","position":"sticky","top":"0","zIndex":"10"}),
            # Dynamic content filled by callback
            html.Div(id="admin-panel-content",children=[
                html.Div("Loading…",style={"color":TEXT_MUTED,"fontSize":"0.8em","padding":"20px"})
            ]),
        ]),

        # ── NEWS PANEL (fixed overlay) ──────────────────────────────────────
        html.Div(id="news-panel",style=NEWS_PANEL_HIDDEN,children=[
            html.Div([html.Div([html.Div("📡",style={"fontSize":"1.1em","marginRight":"8px"}),html.Div([html.Div("GLOBAL MARKET PULSE",style={"color":TEXT_MAIN,"fontWeight":"700","fontSize":"0.72em","letterSpacing":"2px"}),html.Div(id="news-last-updated",style={"color":TEXT_MUTED,"fontSize":"0.58em","marginTop":"1px"})])],style={"display":"flex","alignItems":"center","flex":"1"}),html.Div([html.Button("↺",id="news-refresh-btn",n_clicks=0,style={"backgroundColor":"transparent","border":f"1px solid {BORDER}","color":TEXT_DIM,"padding":"4px 10px","borderRadius":"5px","fontSize":"0.8em","cursor":"pointer","marginRight":"6px"}),html.Button("✕",id="news-close-btn",n_clicks=0,style={"backgroundColor":"transparent","border":f"1px solid {BEAR}40","color":BEAR,"padding":"4px 10px","borderRadius":"5px","fontSize":"0.8em","cursor":"pointer"})],style={"display":"flex","alignItems":"center"})],style={"display":"flex","alignItems":"center","padding":"14px 16px","borderBottom":f"1px solid {BORDER}","backgroundColor":"#060510","position":"sticky","top":"0","zIndex":"10"}),
            html.Div(id="news-content",className="news-panel-scroll",style={"overflowY":"auto","height":"calc(100vh - 60px)","padding":"0 14px 20px 14px"}),dcc.Loading(type="circle",color=PURPLE,children=html.Div(id="news-content",className="news-panel-scroll",style={"overflowY":"auto","height":"calc(100vh - 60px)","padding":"0 14px 20px 14px"})),
        ]),

        # ── AI LAB PANEL (fixed overlay, z=160) ────────────────────────────
        html.Div(id="ailab-panel",style=AILAB_PANEL_HIDDEN,children=[
            # Header
            html.Div([
                html.Div([
                    html.Span("🧠",style={"fontSize":"1.1em","marginRight":"8px"}),
                    html.Div([
                        html.Div("AI LAB",style={"color":TEXT_MAIN,"fontWeight":"700","fontSize":"0.72em","letterSpacing":"2px"}),
                        html.Div("Backtesting · ML Model · Insights",style={"color":TEXT_MUTED,"fontSize":"0.58em","marginTop":"1px"}),
                    ]),
                ],style={"display":"flex","alignItems":"center","flex":"1"}),
                html.Button("✕",id="ailab-close-btn",n_clicks=0,style={"backgroundColor":"transparent","border":f"1px solid {BEAR}40","color":BEAR,"padding":"4px 10px","borderRadius":"5px","fontSize":"0.8em","cursor":"pointer"}),
            ],style={"display":"flex","alignItems":"center","padding":"14px 16px","borderBottom":f"1px solid {BORDER}","backgroundColor":"#060510","position":"sticky","top":"0","zIndex":"10"}),

            html.Div(id="ailab-content",className="ailab-scroll",
                     style={"padding":"14px 16px 40px 16px"},
                     children=[html.Div("Loading…",style={"color":TEXT_MUTED,"fontSize":"0.8em"})]),
        ]),

        # ── TRADE MODAL ─────────────────────────────────────────────────────
        html.Div(id="trade-modal",style={"display":"none"}),
        # ── MAIN CONTENT ────────────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Div([
                    html.Div(id="signal-text",style={"fontSize":"3.4em","fontWeight":"900","letterSpacing":"-2.5px","lineHeight":"1"}),
                    html.Div(id="confidence-div",style={"marginTop":"6px"}),
                    html.Div(id="ml-score-div",style={"marginTop":"5px"}),
                    html.Div(id="signal-sub",style={"color":TEXT_DIM,"fontSize":"0.7em","marginTop":"4px"}),
                    html.Div(id="buy-btn-div",style={"marginTop":"10px"}),
                    html.Div([
                        html.Span("⚡ ", style={"color":NEUTRAL,"fontSize":"0.55em"}),
                        html.Span("Engine is a guide, not a guarantee. Your intuition counts.", style={"color":TEXT_MUTED,"fontSize":"0.55em","fontStyle":"italic","lineHeight":"1.5"}),
                    ], style={"marginTop":"10px","paddingTop":"8px","borderTop":f"1px solid {BORDER}","lineHeight":"1.5"}),
                ],style={"background":"linear-gradient(135deg,#12101d 0%,#0d0c18 100%)","border":"1px solid rgba(147,51,234,0.22)","borderRadius":"14px","padding":"20px 22px","minWidth":"175px","boxShadow":"0 8px 40px rgba(147,51,234,0.15), inset 0 1px 0 rgba(255,255,255,0.04)"}),
                html.Div([
                    html.Div([lbl("Trend"),html.Div(id="trend-text",style={"color":TEXT_MAIN,"fontWeight":"600","fontSize":"1.05em"})],style={"backgroundColor":BG_CARD2,"border":f"1px solid {BORDER}","borderRadius":"10px","padding":"13px 16px","flex":"1"}),
                    html.Div([lbl("RSI  14"),html.Div(id="rsi-text",style={"color":TEXT_MAIN,"fontWeight":"600","fontSize":"1.05em"}),html.Div(id="rsi-hint",style={"color":TEXT_DIM,"fontSize":"0.68em","marginTop":"1px"})],style={"backgroundColor":BG_CARD2,"border":f"1px solid {BORDER}","borderRadius":"10px","padding":"13px 16px","flex":"1"}),
                    html.Div([lbl("MACD"),html.Div(id="macd-text",style={"color":TEXT_MAIN,"fontWeight":"600","fontSize":"1.05em"}),html.Div(id="macd-hint",style={"fontSize":"0.68em","marginTop":"1px"})],style={"backgroundColor":BG_CARD2,"border":f"1px solid {BORDER}","borderRadius":"10px","padding":"13px 16px","flex":"1"}),
                    html.Div([html.Div(id="market-summary",style={"fontFamily":"'Georgia',serif","fontSize":"0.86em","color":TEXT_DIM,"fontStyle":"italic","lineHeight":"1.7"})],style={"backgroundColor":BG_CARD2,"border":f"1px solid {BORDER}","borderRadius":"10px","padding":"13px 16px","flex":"2.2"}),
                ],style={"display":"flex","gap":"7px","flex":"1"}),
            ],style={"display":"flex","gap":"7px","marginBottom":"7px"}),

            html.Div(id="forecast-div"),
            html.Div(id="trade-panel",style={"display":"none"},children=[html.Div([
                html.Div([lbl("Entry Price"),html.Div(id="entry-text",style={"color":TEXT_MAIN,"fontWeight":"600","fontSize":"1.08em"}),html.Div(id="position-size-display",style={"color":TEXT_MUTED,"fontSize":"0.65em"})],style={"backgroundColor":BG_CARD2,"border":"1px solid #1e3a5f","borderRadius":"8px","padding":"11px 15px","flex":"1"}),
                html.Div([
                    html.Div([lbl("Take Profit  🎯"),
                        html.Button("\u29c9",id="copy-tp-btn",n_clicks=0,title="Copy TP",
                            style={"background":"transparent","border":f"1px solid {BULL}40","color":BULL,
                                   "borderRadius":"4px","padding":"1px 6px","fontSize":"0.7em","cursor":"pointer",
                                   "marginLeft":"6px","verticalAlign":"middle"})],
                        style={"display":"flex","alignItems":"center","marginBottom":"2px"}),
                    html.Div(id="tp-text",style={"color":BULL,"fontWeight":"600","fontSize":"1.08em"}),
                    html.Div(id="tp-pnl-preview",style={"color":BULL,"fontSize":"0.65em"}),
                ],style={"backgroundColor":BG_CARD2,"border":"1px solid rgba(52,211,153,0.2)","borderRadius":"8px","padding":"11px 15px","flex":"1"}),
                html.Div([
                    html.Div([lbl("Stop Loss  🛑"),
                        html.Button("\u29c9",id="copy-sl-btn",n_clicks=0,title="Copy SL",
                            style={"background":"transparent","border":f"1px solid {BEAR}40","color":BEAR,
                                   "borderRadius":"4px","padding":"1px 6px","fontSize":"0.7em","cursor":"pointer",
                                   "marginLeft":"6px","verticalAlign":"middle"})],
                        style={"display":"flex","alignItems":"center","marginBottom":"2px"}),
                    html.Div(id="sl-text",style={"color":BEAR,"fontWeight":"600","fontSize":"1.08em"}),
                    html.Div(id="sl-pnl-preview",style={"color":BEAR,"fontSize":"0.65em"}),
                ],style={"backgroundColor":BG_CARD2,"border":"1px solid rgba(248,113,113,0.2)","borderRadius":"8px","padding":"11px 15px","flex":"1"}),
                html.Button("EXIT & LOG TRADE",id="exit-btn",n_clicks=0,className="exit-log-btn",style={"backgroundColor":"rgba(248,113,113,0.08)","border":"1px solid rgba(248,113,113,0.35)","color":BEAR,"fontSize":"0.7em","fontWeight":"700","letterSpacing":"1.2px","padding":"6px 10px","borderRadius":"6px","marginTop":"9px","width":"100%","cursor":"pointer","transition":"all 0.18s ease"})
],style={"display":"flex","gap":"8px","marginBottom":"8px"})]),
            # ── CHART ROW: [pattern sidebar] + [chart card] ──────────────────
            html.Div([
                # ── PATTERN SIDEBAR (hidden by default, shown beside chart) ──
                html.Div(id="pattern-panel",style={"display":"none"},children=[
                    html.Div([
                        # Header
                        html.Div("PATTERNS",style={"color":TEXT_MUTED,"fontSize":"0.52em","letterSpacing":"2px","fontWeight":"700","marginBottom":"10px","paddingBottom":"6px","borderBottom":f"1px solid {BORDER}"}),
                        # Color legend
                        html.Div([
                            html.Span("▮",style={"color":BULL,"marginRight":"4px","fontSize":"0.7em"}),html.Span("Bullish",style={"color":TEXT_MUTED,"fontSize":"0.6em","marginRight":"8px"}),
                            html.Span("▮",style={"color":BEAR,"marginRight":"4px","fontSize":"0.7em"}),html.Span("Bearish",style={"color":TEXT_MUTED,"fontSize":"0.6em","marginRight":"8px"}),
                            html.Span("▮",style={"color":NEUTRAL,"marginRight":"4px","fontSize":"0.7em"}),html.Span("Neutral",style={"color":TEXT_MUTED,"fontSize":"0.6em"}),
                        ],style={"marginBottom":"10px","display":"flex","flexWrap":"wrap","alignItems":"center"}),
                        # Chips grid
                        html.Div(id="pattern-toggle-container",children=make_toggles([]),
                            style={"marginBottom":"14px"}),
                        # Divider
                        html.Div(style={"height":"1px","backgroundColor":BORDER,"margin":"6px 0 10px 0"}),
                        # Active on chart
                        html.Div("ACTIVE ON CHART",style={"color":TEXT_MUTED,"fontSize":"0.52em","letterSpacing":"2px","fontWeight":"700","marginBottom":"8px"}),
                        html.Div(id="active-pattern-list",children=make_active_list([])),
                    ],style={"padding":"12px 10px","overflowY":"auto","height":"100%"}),
                ]),

                # ── CHART CARD ────────────────────────────────────────────────
                html.Div([
                    html.Div(id="alert-triggered-bar",style={"display":"none"},children=[html.Div("🔔  PRICE ALERT TRIGGERED!",style={"backgroundColor":f"{PURPLE}30","border":f"1px solid {PURPLE}","color":NEUTRAL,"padding":"8px 16px","fontSize":"0.82em","fontWeight":"600","textAlign":"center","letterSpacing":"1px"})]),
                    # Chart toolbar — pattern picker + indicator toggles
                    html.Div([
                        tbtn("⊞ Patterns","pattern-btn",tip="Open pattern picker"),
                        html.Div(style={"width":"1px","height":"18px","backgroundColor":BORDER,"margin":"0 8px","flexShrink":"0"}),
                        tbtn("〰 Bands","bb-btn",tip="Toggle Bollinger Bands on chart"),
                        html.Div(style={"width":"4px"}),
                        tbtn("📏 Pivots","pd-btn",tip="Toggle Pivot / Divergence lines on chart"),
                        *([html.Div(style={"width":"4px"}),tbtn("📊 Breakdown","breakdown-btn",tip="Open signal breakdown panel")] if limits["breakdown"] else []),
                    ],style={"display":"flex","alignItems":"center","padding":"6px 10px","borderBottom":f"1px solid {BORDER}","backgroundColor":"#07060f"}),
                    html.Div([
                        dcc.Graph(id="candle-chart",style={"height":"620px","flex":"1","minWidth":"0"},config={
                            "scrollZoom":True,
                            "displayModeBar":False,   # hide modebar — stops hover reflow jank
                            "doubleClick":"reset",
                            "responsive":True,
                            "showTips":False,
                        }),
                        html.Div(id="breakdown-panel",className="breakdown-scroll",style=BREAKDOWN_HIDDEN,children=[html.Div(id="breakdown-content")]),
                    ],style={"display":"flex"}),
                ],style={"flex":"1","backgroundColor":BG_CARD2,"border":f"1px solid {BORDER}","borderRadius":"10px","minWidth":"0"}),

            ],style={"display":"flex","gap":"7px","marginBottom":"7px","alignItems":"flex-start"}),

            html.Div(id="last-updated",style={"color":TEXT_MUTED,"fontSize":"0.6em","textAlign":"right","marginBottom":"10px"}),
            html.Div([
                html.Div([html.Div("PATTERNS DETECTED",style={"color":TEXT_MAIN,"fontSize":"0.6em","letterSpacing":"1.5px","fontWeight":"600","marginBottom":"10px","opacity":"0.85"}),html.Div(id="patterns-div")],style={"backgroundColor":BG_CARD2,"border":f"1px solid {BORDER}","borderRadius":"10px","padding":"16px 18px","flex":"1"}),
                html.Div([html.Div("TIPS & LESSONS",style={"color":TEXT_MAIN,"fontSize":"0.6em","letterSpacing":"1.5px","fontWeight":"600","marginBottom":"10px","opacity":"0.85"}),html.Div(id="tips-div")],style={"backgroundColor":BG_CARD2,"border":f"1px solid {BORDER}","borderRadius":"10px","padding":"16px 18px","flex":"1"}),
            ],style={"display":"flex","gap":"7px","marginBottom":"7px"}),
            html.Div([html.Div("RECENT PATTERN HISTORY",style={"color":TEXT_MAIN,"fontSize":"0.6em","letterSpacing":"1.5px","fontWeight":"600","marginBottom":"10px","opacity":"0.85"}),html.Div(id="pattern-history-div")],style={"backgroundColor":BG_CARD2,"border":f"1px solid {BORDER}","borderRadius":"10px","padding":"16px 18px","marginBottom":"20px"}),
        ],style={"padding":"10px 24px"}),

        html.Div([html.Span("BOJKET  ",style={"color":PURPLE,"fontWeight":"700","letterSpacing":"2px","fontSize":"0.7em"}),html.Span("·  The future of trading.  ·  ",style={"color":TEXT_MUTED,"fontSize":"0.62em","fontStyle":"italic"}),html.Span("Not financial advice. Trade responsibly.",style={"color":TEXT_MUTED,"fontSize":"0.6em"})],style={"borderTop":f"1px solid {BORDER}","padding":"14px 24px","display":"flex","alignItems":"center","gap":"4px","backgroundColor":"#050508"}),

        # ── CHAT ─────────────────────────────────────────────────────────────
        html.Div([
            html.Div(id="chat-panel",style={"display":"none","width":"380px","backgroundColor":"#0a0912","border":f"1px solid {BORDER}","borderRadius":"14px","overflow":"hidden","boxShadow":"0 8px 40px rgba(0,0,0,0.6)"},children=[
                html.Div([html.Div([html.Span("✦",style={"color":PURPLE,"marginRight":"8px","fontSize":"1.1em"}),html.Span("Bojket",style={"color":TEXT_MAIN,"fontWeight":"600","fontSize":"0.9em"}),html.Span("●",style={"color":BULL,"fontSize":"0.45em","marginLeft":"8px","verticalAlign":"middle"}),html.Span("online",style={"color":TEXT_MUTED,"fontSize":"0.6em","marginLeft":"4px"})],style={"display":"flex","alignItems":"center","flex":"1"}),html.Span("✕",id="chat-close-btn",n_clicks=0,style={"cursor":"pointer","color":TEXT_MUTED,"fontSize":"1em","padding":"2px 6px","userSelect":"none"})],style={"display":"flex","alignItems":"center","padding":"11px 14px","borderBottom":f"1px solid {BORDER}"}),
                html.Div(id="chat-messages-area",className="chat-scroll",children=render_chat_messages([]),style={"height":"400px","overflowY":"auto","padding":"12px","display":"flex","flexDirection":"column","gap":"8px"}),
                html.Div([dcc.Input(id="chat-input",type="text",placeholder="Ask Bojket anything...",debounce=False,n_submit=0,style={"flex":"1","backgroundColor":"transparent","border":"none","color":TEXT_MAIN,"fontSize":"0.82em","outline":"none","padding":"8px 0"}),html.Button("→",id="chat-send-btn",n_clicks=0,style={"backgroundColor":PURPLE,"border":"none","color":"white","padding":"7px 13px","borderRadius":"8px","cursor":"pointer","fontSize":"0.9em","fontWeight":"600"})],style={"display":"flex","alignItems":"center","padding":"8px 14px","borderTop":f"1px solid {BORDER}","gap":"8px"}),
                html.Div([
                    html.Button("🎓 Replay Tutorial",id="tutorial-replay-btn",n_clicks=0,style={"backgroundColor":"transparent","border":"none","color":TEXT_MUTED,"fontSize":"0.62em","cursor":"pointer","padding":"4px 8px","textDecoration":"underline"}),
                ],style={"padding":"0 14px 6px 14px","textAlign":"center"}),
            ]),
            html.Div([html.Span("✦",style={"color":"white","marginRight":"7px","fontSize":"1.0em"}),html.Span("Bojket",style={"color":"white","fontWeight":"500","fontSize":"0.82em","letterSpacing":"1px"})],id="chat-toggle-btn",n_clicks=0,style={"display":"flex","alignItems":"center","backgroundColor":PURPLE,"padding":"9px 18px","borderRadius":"20px","cursor":"pointer","userSelect":"none","boxShadow":f"0 4px 20px {PURPLE_GLOW}"}),
        ],style={"position":"fixed","bottom":"24px","right":"24px","zIndex":"1000","display":"flex","flexDirection":"column","alignItems":"flex-end","gap":"8px"}),

        # ── STORES & INTERVALS ───────────────────────────────────────────────
        dcc.Interval(id="auto-refresh",    interval=60*1000, n_intervals=0),
        dcc.Interval(id="ml-poll-interval", interval=2500,  n_intervals=0),
        dcc.Store(id="trade-store",data={"in_trade":False,"entry":None,"signal":None,"symbol":None,"time":None,"position_size":None,"custom_tp":None,"custom_sl":None,"tp":None,"sl":None,"cooldown":False,"cooldown_since":None,"last_result":None,"consecutive_losses":0}),
        dcc.Store(id="active-patterns-store",data=[]),
        dcc.Store(id="journal-store",data=[]),
        dcc.Store(id="chart-theme",data="dark"),
        dcc.Store(id="bb-store",data=False),
        dcc.Store(id="pd-store",data=False),
        dcc.Store(id="alert-store",data={"price":None,"active":False}),
        dcc.Store(id="mute-store",data=False),
        dcc.Store(id="bell-dd-store",data=False),
        dcc.Store(id="pattern-history-store",data=[]),
        dcc.Store(id="chat-messages-store",data=[]),
        dcc.Store(id="chat-open-store",data=False),
        dcc.Store(id="chat-pending-store",data=None),
        dcc.Store(id="quick-chip-store",data=""),
        dcc.Store(id="pending-trade-store",data=None),
        dcc.Store(id="breakdown-open-store",data=False),
        dcc.Store(id="ailab-open-store",data=False),
        dcc.Store(id="bt-symbol-store",data="BTC-USD"),
        dcc.Store(id="bt-interval-store",data="1h"),
        dcc.Store(id="ml-train-symbols-store",data=["BTC-USD","ETH-USD","SOL-USD","NQ=F","GC=F","EURUSD=X"]),
        dcc.Store(id="ml-train-interval-store",data="1h"),
    ],style={"backgroundColor":BG_DARK,"minHeight":"100vh","color":TEXT_MAIN})


