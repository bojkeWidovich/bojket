# ══════════════════════════════════════════════════════════════════════════════
#  payment.py  —  PayPal subscription routes mounted on Flask server
#  To activate: fill in PAYPAL_* values in config.py, set PAYPAL_SANDBOX=False
# ══════════════════════════════════════════════════════════════════════════════

import requests as http_req
from flask import redirect as _flask_redirect, request as _flask_req

from server import server
from config import (
    PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, PAYPAL_SANDBOX,
    PAYPAL_PLAN_HUSTLER_MO, PAYPAL_PLAN_HUSTLER_YR,
    PAYPAL_PLAN_VETERAN_MO, PAYPAL_PLAN_VETERAN_YR,
    _register_user,
)



# ── Flask imports needed for payment routes ───────────────────────────────────
from flask import redirect as _flask_redirect, request as _flask_req

# ── PayPal helpers ────────────────────────────────────────────────────────────
def _pp_base():
    return "https://api-m.sandbox.paypal.com" if PAYPAL_SANDBOX else "https://api-m.paypal.com"

def _pp_token():
    """Exchange client credentials for a short-lived bearer token."""
    r = http_req.post(
        f"{_pp_base()}/v1/oauth2/token",
        headers={"Accept": "application/json"},
        auth=(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET),
        data={"grant_type": "client_credentials"},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()["access_token"]

def _pp_configured():
    return not PAYPAL_CLIENT_ID.startswith("YOUR_")

@server.route("/create-checkout-session")
def _create_checkout():
    plan    = _flask_req.args.get("plan",    "hustler")
    billing = _flask_req.args.get("billing", "monthly")
    email   = _flask_req.args.get("email",   "")
    # Dev mode — skip PayPal and grant access immediately
    if not _pp_configured():
        return _flask_redirect(f"/payment-complete?plan={plan}&billing={billing}&email={email}")
    plan_map = {
        ("hustler","monthly"): PAYPAL_PLAN_HUSTLER_MO,
        ("hustler","annual"):  PAYPAL_PLAN_HUSTLER_YR,
        ("veteran","monthly"): PAYPAL_PLAN_VETERAN_MO,
        ("veteran","annual"):  PAYPAL_PLAN_VETERAN_YR,
    }
    plan_id = plan_map.get((plan, billing), PAYPAL_PLAN_HUSTLER_MO)
    try:
        token    = _pp_token()
        ret_url  = _flask_req.host_url + f"payment-complete?plan={plan}&billing={billing}&email={email}"
        cancel   = _flask_req.host_url + "pricing"
        payload  = {
            "plan_id": plan_id,
            "application_context": {
                "brand_name":  "Bojket",
                "return_url":  ret_url,
                "cancel_url":  cancel,
                "user_action": "SUBSCRIBE_NOW",
            },
        }
        if email:
            payload["subscriber"] = {"email_address": email}
        resp = http_req.post(
            f"{_pp_base()}/v1/billing/subscriptions",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=payload,
            timeout=15,
        )
        resp.raise_for_status()
        for link in resp.json().get("links", []):
            if link.get("rel") == "approve":
                return _flask_redirect(link["href"], code=303)
        return "PayPal error: no approval URL returned", 400
    except Exception as ex:
        return f"PayPal error: {ex}", 400

@server.route("/payment-complete")
def _payment_complete():
    plan            = _flask_req.args.get("plan",            "hustler")
    billing         = _flask_req.args.get("billing",         "monthly")
    email           = _flask_req.args.get("email",           "")
    subscription_id = _flask_req.args.get("subscription_id", "")
    # Verify subscription status with PayPal when configured
    if _pp_configured() and subscription_id:
        try:
            token = _pp_token()
            r = http_req.get(
                f"{_pp_base()}/v1/billing/subscriptions/{subscription_id}",
                headers={"Authorization": f"Bearer {token}"},
                timeout=15,
            )
            if r.ok:
                status = r.json().get("status", "")
                if status not in ("ACTIVE", "APPROVED"):
                    return _flask_redirect("/pricing")
        except Exception:
            pass
    if email:
        _register_user(email, plan, billing)
    return _flask_redirect(f"/dashboard?post_payment=1&plan={plan}&billing={billing}&email={email}")

@server.route("/webhook", methods=["POST"])
def _paypal_webhook():
    """PayPal sends BILLING.SUBSCRIPTION.ACTIVATED when payment clears."""
    event = _flask_req.get_json(silent=True) or {}
    if event.get("event_type") == "BILLING.SUBSCRIPTION.ACTIVATED":
        resource = event.get("resource", {})
        sub_id   = resource.get("id", "")
        # Look up subscriber email from PayPal if configured
        if _pp_configured() and sub_id:
            try:
                token = _pp_token()
                r = http_req.get(
                    f"{_pp_base()}/v1/billing/subscriptions/{sub_id}",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=15,
                )
                if r.ok:
                    data    = r.json()
                    em      = data.get("subscriber", {}).get("email_address", "")
                    plan_id = data.get("plan_id", "")
                    # Map plan_id back to internal plan name
                    rev_map = {
                        PAYPAL_PLAN_HUSTLER_MO: ("hustler","monthly"),
                        PAYPAL_PLAN_HUSTLER_YR: ("hustler","annual"),
                        PAYPAL_PLAN_VETERAN_MO: ("veteran","monthly"),
                        PAYPAL_PLAN_VETERAN_YR: ("veteran","annual"),
                    }
                    pl, bi = rev_map.get(plan_id, ("hustler","monthly"))
                    if em:
                        _register_user(em, pl, bi)
            except Exception:
                pass
    return "OK", 200
