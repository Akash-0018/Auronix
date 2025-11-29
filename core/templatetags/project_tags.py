from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def get_project_placeholder(project_title):
    """Returns appropriate placeholder image path based on project title keywords"""
    title = project_title.lower()
    
    if 'e-commerce' in title or 'ecommerce' in title:
        return 'images/project-placeholder-ecommerce.svg'
    elif 'mobile' in title or 'app' in title or 'fit' in title or 'track' in title:
        return 'images/project-placeholder-mobile.svg'
    elif 'brand' in title or 'identity' in title or 'techn' in title:
        return 'images/project-placeholder-branding.svg'
    elif 'crm' in title or 'customer' in title or 'client' in title or 'sync' in title:
        return 'images/project-placeholder-crm.svg'
    elif 'travel' in title or 'booking' in title or 'eco' in title:
        return 'images/project-placeholder-travel.svg'
    elif 'finance' in title or 'financial' in title or 'budget' in title or 'fin' in title:
        return 'images/project-placeholder-finance.svg'
    elif 'cafe' in title or 'coffee' in title or 'restaurant' in title or 'artisan' in title:
        return 'images/project-placeholder-cafe.svg'
    elif 'health' in title or 'medical' in title or 'patient' in title or 'medi' in title:
        return 'images/project-placeholder-healthcare.svg'
    elif 'blog' in title:
        return 'images/project-placeholder-blog.svg'
    elif 'corporate' in title or 'company' in title:
        return 'images/project-placeholder-corporate.svg'
    else:
        return 'images/project-placeholder-branding.svg'

@register.filter
def clean_phone(phone_number):
    """
    Removes spaces, hyphens, and special characters from phone number.
    Useful for creating WhatsApp links.
    
    Example:
    '+91 98434 64180' -> '+919843464180'
    """
    if not phone_number:
        return ''
    # Remove spaces, hyphens, parentheses, and dots
    import re
    cleaned = re.sub(r'[\s\-\(\)\.]', '', str(phone_number))
    return cleaned