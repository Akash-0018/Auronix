from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.contrib.auth.models import User
from django.db.models import Q


class NoIntermediarySocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom adapter to skip the intermediate confirmation page and auto-link existing users"""
    
    def pre_social_login(self, request, sociallogin):
        """
        Auto-connect existing users with matching email addresses
        """
        # If the account already exists, return (already connected)
        if sociallogin.is_existing:
            return
        
        # Try to find an existing user with the same email
        if sociallogin.email_addresses:
            for email in sociallogin.email_addresses:
                if email.verified:
                    # Search for existing user with this email
                    try:
                        existing_user = User.objects.get(email=email.email)
                        # Connect the social account to the existing user
                        sociallogin.connect(request, existing_user)
                        return
                    except User.DoesNotExist:
                        # No existing user with this email, continue with signup
                        pass
    
    def is_auto_signup_allowed(self, request, sociallogin):
        """Always auto-signup new users from Google"""
        return True
