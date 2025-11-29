from django.conf import settings
from allauth.socialaccount.models import SocialApp


def google_oauth_context(request):
    """
    Add Google OAuth availability to all templates.
    This prevents DoesNotExist errors when Google OAuth app is not configured.
    """
    try:
        google_app = SocialApp.objects.get(provider='google')
        google_oauth_available = True
    except SocialApp.DoesNotExist:
        google_oauth_available = False
    except Exception:
        google_oauth_available = False

    return {
        'google_oauth_available': google_oauth_available,
    }
