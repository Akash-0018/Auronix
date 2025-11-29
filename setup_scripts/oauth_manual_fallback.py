#!/usr/bin/env python
"""
Simple OAuth 2.0 token generator - Manual authorization
Generates token.pickle for Google Calendar API without needing a local server
"""
import os
import sys
import pickle
import json
from pathlib import Path
from urllib.parse import urlencode, urlparse, parse_qs

# Setup Django
sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

import django
django.setup()

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/calendar']

def manual_oauth_setup():
    """
    Manual OAuth setup - User authorizes in browser and pastes code
    More reliable than trying to run a local server
    """
    
    # Get credentials from environment
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ Error: GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET not in .env")
        return False
    
    # Create temporary credentials.json
    core_dir = Path(__file__).parent
    credentials_file = core_dir / 'credentials.json'
    
    # Use a simple localhost callback URI
    redirect_uri = 'http://localhost:8080/'
    
    credentials_dict = {
        'installed': {
            'client_id': client_id,
            'client_secret': client_secret,
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'redirect_uris': [redirect_uri],
            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs'
        }
    }
    
    try:
        with open(credentials_file, 'w') as f:
            json.dump(credentials_dict, f, indent=2)
        print("✓ Created credentials configuration")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    try:
        print("\n" + "="*70)
        print("🔐 GOOGLE CALENDAR OAUTH AUTHORIZATION")
        print("="*70)
        
        flow = InstalledAppFlow.from_client_secrets_file(
            str(credentials_file),
            SCOPES
        )
        
        print("\n📱 Starting authorization flow...")
        print("✓ Browser window opening...\n")
        
        # This opens browser and waits for callback
        credentials = flow.run_local_server(
            port=8080,
            open_browser=True,
            authorization_prompt_message='Authorizing Serendipity Portfolio to access Google Calendar'
        )
        
        # Save token.pickle
        token_file = core_dir / 'token.pickle'
        with open(token_file, 'wb') as token:
            pickle.dump(credentials, token)
        
        print("\n✅ SUCCESS!")
        print(f"✓ Token saved: {token_file}")
        print("✓ OAuth is now configured!")
        print("\n🎉 Real Google Meet integration ready!")
        print("   - Google Calendar events will be created automatically")
        print("   - Real Google Meet links will be generated")
        print("   - Emails will contain actual meeting links")
        
        # Clean up
        try:
            os.remove(credentials_file)
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"\n❌ Authorization failed: {e}")
        
        # Check if it's a redirect_uri_mismatch error
        if 'redirect_uri_mismatch' in str(e):
            print("\n🔧 REDIRECT URI MISMATCH ERROR")
            print("="*70)
            print("This means the redirect URI in Google Cloud Console doesn't match.")
            print("\nTo fix:")
            print("1. Go to: https://console.cloud.google.com/")
            print("2. Select your project")
            print("3. Go to: APIs & Services → Credentials")
            print("4. Click on your OAuth 2.0 Client ID")
            print("5. Under 'Authorized redirect URIs', add:")
            print("   • http://localhost:8080/")
            print("   • http://127.0.0.1:8080/")
            print("6. Save and try again")
        
        # Clean up
        try:
            if credentials_file.exists():
                os.remove(credentials_file)
        except:
            pass
        
        return False


if __name__ == '__main__':
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  GOOGLE CALENDAR OAUTH SETUP".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    # Check if token already exists
    core_dir = Path(__file__).parent
    token_file = core_dir / 'token.pickle'
    
    if token_file.exists():
        print(f"\n✓ Token already exists at: {token_file}")
        response = input("\nDo you want to refresh it? (y/n): ").lower().strip()
        if response != 'y':
            print("\nExiting without changes.")
            sys.exit(0)
    
    success = manual_oauth_setup()
    
    if success:
        print("\n" + "="*70)
        print("Next steps:")
        print("1. Start Django server: python manage.py runserver")
        print("2. Go to admin: http://localhost:8000/admin/core/meeting/")
        print("3. Create a test meeting and generate Meet link")
        print("="*70 + "\n")
        sys.exit(0)
    else:
        print("\n" + "="*70)
        print("Setup failed. Please fix the errors above and try again.")
        print("="*70 + "\n")
        sys.exit(1)
