#!/usr/bin/env python
"""
Google OAuth 2.0 Token Setup (WEB APPLICATION FLOW)
Creates token.pickle as REAL Credentials object for use with Google Calendar + Meet
"""

import os
import sys
import json
import pickle
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import requests
from google.oauth2.credentials import Credentials

# Make Django imports available
sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio.settings")

import django
django.setup()

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events"
]


# ----------------------------------------------------------
# AUTH URL
# ----------------------------------------------------------
def build_authorization_url(client_id, redirect_uri, state):
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
        "state": state
    }

    base = "https://accounts.google.com/o/oauth2/auth"
    query = "&".join(f"{k}={requests.utils.quote(v)}" for k, v in params.items())
    return f"{base}?{query}"


# ----------------------------------------------------------
# TOKEN EXCHANGE
# ----------------------------------------------------------
def exchange_code_for_token(client_id, client_secret, redirect_uri, code):
    token_url = "https://oauth2.googleapis.com/token"

    payload = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }

    r = requests.post(token_url, data=payload)
    if r.status_code != 200:
        print("\n❌ Token exchange failed:")
        print(r.text)
        return None

    return r.json()


# ----------------------------------------------------------
# MAIN SETUP FUNCTION
# ----------------------------------------------------------
def run_oauth_setup():
    print("=" * 60)
    print(" GOOGLE OAUTH 2.0 (WEB FLOW FOR GOOGLE MEET) ")
    print("=" * 60)

    # Load env vars
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    redirect_uris = os.getenv("GOOGLE_OAUTH_REDIRECT_URIS", "").split(",")

    redirect_uri = redirect_uris[0].strip() if redirect_uris else None

    if not client_id or not client_secret or not redirect_uri:
        print("\n❌ Missing GOOGLE_CLIENT_ID, SECRET, or REDIRECT_URIS")
        return

    print(f"Client ID: {client_id}")
    print(f"Redirect URI: {redirect_uri}")

    # Save credentials.json for reference
    credentials_file = Path(__file__).parent / "credentials.json"
    credentials_file.write_text(json.dumps({
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": [redirect_uri],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }, indent=2))

    print("✓ credentials.json created\n")

    # Build URL
    import uuid
    state = uuid.uuid4().hex

    auth_url = build_authorization_url(client_id, redirect_uri, state)

    print("\n👉 Open this URL:")
    print(auth_url)
    print("\nAfter authorizing, paste the FULL redirect URL below:\n")

    redirect_response = input("Redirect URL: ").strip()

    # Parse response
    parsed = urlparse(redirect_response)
    qs = parse_qs(parsed.query)

    returned_state = qs.get("state", [""])[0]
    code = qs.get("code", [""])[0]

    if state != returned_state:
        print("\n❌ STATE mismatch – stopping")
        return

    if not code:
        print("\n❌ No authorization code found")
        return

    print("\n🔄 Exchanging authorization code...\n")

    # Exchange token
    token_data = exchange_code_for_token(client_id, client_secret, redirect_uri, code)
    if not token_data:
        return

    # ------------------------------------------------------
    # FIX: SAVE REAL GOOGLE CREDENTIALS OBJECT
    # ------------------------------------------------------
    creds = Credentials(
        token=token_data.get("access_token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES
    )

    token_path = Path(__file__).parent / "token.pickle"
    with open(token_path, "wb") as f:
        pickle.dump(creds, f)

    print("\n🎉 SUCCESS!")
    print(f"✓ token.pickle saved → {token_path}")
    print("✓ OAuth COMPLETE")
    print("✓ Google Meet API READY ✔")


# ----------------------------------------------------------
# ENTRY POINT
# ----------------------------------------------------------
if __name__ == "__main__":
    token_path = Path(__file__).parent / "token.pickle"

    print("=" * 60)
    print(" GOOGLE CALENDAR + MEET OAUTH SETUP ")
    print("=" * 60)

    if token_path.exists():
        print(f"\nExisting token found: {token_path}")
        if input("Refresh? (y/n): ").lower() != "y":
            print("\nExiting.")
            sys.exit(0)

    run_oauth_setup()

    print("\n" + "=" * 60)
    print(" DONE! ")
    print("=" * 60)
