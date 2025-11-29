from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin


class NoIntermediarySocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom adapter to skip the intermediate confirmation page"""
    
    def pre_social_login(self, request, sociallogin):
        """
        Skip the confirmation page and auto-connect existing email accounts
        """
        # If the email already exists, connect it automatically
        if sociallogin.is_existing:
            return
        
        if sociallogin.email_addresses:
            for email in sociallogin.email_addresses:
                if email.verified:
                    # Use the verified email from the provider
                    sociallogin.email_addresses[0].primary = True
                    break
    
    def is_auto_signup_allowed(self, request, sociallogin):
        """Always auto-signup new users from Google"""
        return True
