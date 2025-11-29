# OAuth Setup Guide

This directory contains scripts for setting up Google OAuth 2.0 credentials for the Calendar API integration.

## Quick Start

### Option 1: Automated Setup (Recommended) ✅

```bash
python setup_scripts/oauth_setup.py
```

This will:
1. Generate an authorization URL
2. Ask you to paste the authorization code
3. Create `core/token.pickle` with valid credentials

**Best for**: Most users, no local server required

---

### Option 2: Manual Fallback

If the automated setup fails:

```bash
python setup_scripts/oauth_manual_fallback.py
```

**Best for**: Troubleshooting, alternative authentication flow

---

## What These Scripts Do

### `oauth_setup.py` (Primary Method)
- Generates OAuth 2.0 token using web application flow
- No server startup required
- Creates persistent `token.pickle` file
- **Output**: `core/token.pickle` (add to .gitignore)

### `oauth_manual_fallback.py` (Alternative Method)
- Manual authorization process
- User copies authorization URL to browser
- Pastes code back into terminal
- Creates `token.pickle` for Calendar API access

---

## Important Notes

⚠️ **Security:**
- `token.pickle` contains OAuth credentials - never commit to git
- Add to `.gitignore` (already done in this project)
- Keep `credentials.json` private

⚠️ **Requirements:**
- Google Cloud Project with Calendar API enabled
- OAuth 2.0 credentials file (`core/credentials.json`)
- Python 3.8+

---

## Troubleshooting

### "credentials.json not found"
- Download from Google Cloud Console
- Place in `core/credentials.json`
- Make sure Calendar API is enabled

### "Invalid token"
- Delete `core/token.pickle`
- Re-run setup script
- Re-authorize

### Python module errors
- Install dependencies: `pip install google-auth-oauthlib google-auth-httplib2`

---

## File Organization

```
setup_scripts/
├── oauth_setup.py              ← Use this (recommended)
└── oauth_manual_fallback.py    ← Use if above fails
```

## When to Run Setup

- **First Time**: After cloning the project
- **Token Expired**: If `token.pickle` becomes invalid
- **Credentials Changed**: If you regenerated OAuth credentials

---

## Testing the Setup

Once token is created, verify it works:

```python
python manage.py shell
from core.meeting_utils import get_oauth_credentials
credentials, is_valid = get_oauth_credentials()
print(f"Valid: {is_valid}")  # Should print: Valid: True
```

---

## Integration

These scripts are called by:
- `core/meeting_utils.py` → `get_oauth_credentials()` function
- Automatically loads and refreshes `token.pickle` at runtime

No manual intervention needed after initial setup! 🎉
