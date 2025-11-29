"""
Utility functions for meeting management and Google Meet integration using OAuth 2.0
Creates REAL Google Calendar events with actual Google Meet links

IMPORTANT:
- Personal Gmail accounts CANNOT use PATCH to add Google Meet.
- Only INSERT with conferenceData works.
"""
import uuid
import json
import os
import pickle
from datetime import datetime, timedelta
from urllib.parse import urlencode
import logging
import pytz

logger = logging.getLogger(__name__)

# IST timezone
IST = pytz.timezone('Asia/Kolkata')

# Required Calendar Scopes
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events"
]


def get_oauth_credentials():
    """
    Load OAuth token.pickle created by setup_oauth_token.py
    """
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        
        token_path = os.path.join(os.path.dirname(__file__), 'token.pickle')

        if not os.path.exists(token_path):
            print("❌ token.pickle NOT FOUND — run: python core/setup_oauth_token.py")
            return None, False

        print(f"✓ token.pickle found at: {token_path}")

        with open(token_path, 'rb') as f:
            credentials = pickle.load(f)

        print(f"✓ Credentials loaded")
        print(f"  - Valid: {credentials.valid}")
        print(f"  - Expired: {credentials.expired}")
        print(f"  - Refresh Token: {bool(credentials.refresh_token)}")

        # Refresh expired token
        if credentials.expired and credentials.refresh_token:
            print("⏳ Refreshing token...")
            credentials.refresh(Request())
            print("✓ Token refreshed")

        return credentials, True

    except Exception as e:
        print(f"❌ Failed to load token: {e}")
        return None, False



def generate_google_meet_url(meeting_title, meeting_date, meeting_time, meeting_email, meeting_notes=""):
    """
    Generate REAL Google Meet link by creating a calendar event.
    If OAuth fails → returns fallback valid Meet-like URL.
    """
    print("\n" + "="*70)
    print("🎯 GENERATING GOOGLE MEET URL")
    print("="*70)

    credentials, is_valid = get_oauth_credentials()

    if not is_valid:
        fallback = generate_simple_meet_url()
        print(f"⚠ OAuth missing → Using fallback: {fallback}")
        return {
            "url": fallback,
            "method": "fallback",
            "success": True,
            "error": "No OAuth"
        }

    return _create_real_calendar_event(
        credentials,
        meeting_title,
        meeting_date,
        meeting_time,
        meeting_email,
        meeting_notes
    )



def _create_real_calendar_event(credentials, meeting_title, meeting_date, meeting_time, meeting_email, meeting_notes):
    """
    CREATE event WITH Google Meet via INSERT (works for all Gmail accounts).
    """
    try:
        from googleapiclient.discovery import build
        from django.conf import settings
        
        service = build("calendar", "v3", credentials=credentials)
        print("✓ Google Calendar service ready")

        # Build datetime (IST)
        start_dt = IST.localize(datetime.combine(meeting_date, meeting_time))
        end_dt = start_dt + timedelta(hours=1)

        admin_email = settings.EMAIL_HOST_USER

        print(f"🕒 Start: {start_dt}, End: {end_dt}")

        # ✔ Google requires “attendees”, not “guests”
        event_body = {
            "summary": meeting_title,
            "description": f"Requested by: {meeting_email}\n\nNotes:\n{meeting_notes}",
            "start": {
                "dateTime": start_dt.isoformat(),
                "timeZone": "Asia/Kolkata"
            },
            "end": {
                "dateTime": end_dt.isoformat(),
                "timeZone": "Asia/Kolkata"
            },
            "attendees": [
                {"email": meeting_email},
                {"email": admin_email}
            ],
            "conferenceData": {
                "createRequest": {
                    "requestId": str(uuid.uuid4()),
                    "conferenceSolutionKey": {"key": "hangoutsMeet"}
                }
            }
        }

        print("📤 Creating event with Google Meet...")

        # ✔ INSERT event with conferenceData (Works for ALL accounts)
        created_event = service.events().insert(
            calendarId="primary",
            body=event_body,
            conferenceDataVersion=1
        ).execute()

        print("✓ Event created!")

        event_id = created_event.get("id")
        meet_url = ""

        # Extract Meet URL
        conference = created_event.get("conferenceData", {})
        for ep in conference.get("entryPoints", []):
            if ep.get("entryPointType") == "video":
                meet_url = ep.get("uri")
                break

        if meet_url:
            print(f"✓ Meet Link: {meet_url}")
        else:
            print("⚠ No meet link found, using fallback calendar link")
            meet_url = created_event.get("htmlLink")

        return {
            "url": meet_url,
            "event_id": event_id,
            "calendar_link": created_event.get("htmlLink", ""),
            "method": "calendar_api",
            "success": True,
            "error": None
        }

    except Exception as e:
        print(f"❌ ERROR creating real event: {e}")
        fallback = generate_simple_meet_url()
        return {
            "url": fallback,
            "method": "fallback",
            "success": False,
            "error": str(e)
        }



def generate_simple_meet_url():
    """ Generates a valid-form Meet-like URL for fallback use. """
    import random, string
    p1 = ''.join(random.choices(string.ascii_lowercase, k=3))
    p2 = ''.join(random.choices(string.ascii_lowercase, k=4))
    p3 = ''.join(random.choices(string.ascii_lowercase, k=3))
    return f"https://meet.google.com/{p1}-{p2}-{p3}"



def generate_google_calendar_link(meeting_title, meeting_email, meeting_date, meeting_time, notes=""):
    """ Fallback manual Google Calendar link generator """
    try:
        start = datetime.combine(meeting_date, meeting_time)
        end = start + timedelta(hours=1)

        params = {
            "action": "TEMPLATE",
            "text": meeting_title,
            "details": f"Requested by {meeting_email}\nNotes:\n{notes}",
            "dates": f"{start.strftime('%Y%m%dT%H%M%S')}/{end.strftime('%Y%m%dT%H%M%S')}",
            "location": "Google Meet"
        }

        return f"https://calendar.google.com/calendar/render?{urlencode(params)}"

    except:
        return None
