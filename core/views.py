from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm, MeetingForm, TeamMemberEditForm
from django.urls import reverse
from .models import Project, TeamMember, Meeting
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
import json
import logging

from .models import Testimonial

@login_required(login_url='/accounts/login/')
def home(request):
    # Get the 4 most recent projects
    projects = get_portfolio_projects()[:4]  # Only get the first 4 projects
    testimonials = Testimonial.objects.all()
    return render(request, 'core/home.html', {'section': 'home', 'featured_projects': projects, 'testimonials': testimonials})

def get_portfolio_projects():
    """Returns list of portfolio projects - used by both home and portfolio views"""
    projects = Project.objects.all().order_by('-completion_date')
    project_list = []
    for project in projects:
        # Get main image URL (full-size for modal)
        main_image_url = project.image.url if project.image else 'https://via.placeholder.com/1200x800/7f8c8d/ffffff?text=Project+Image'
        # Get fallback image URL (for card preview)
        fallback_image_url = project.fallback_image.url if project.fallback_image else 'https://via.placeholder.com/400x300/7f8c8d/ffffff?text=Project+Placeholder'
        
        project_list.append({
            'title': project.title,
            'description': project.description,
            'image': main_image_url,
            'fallback_image': fallback_image_url,
            'external_image': project.external_image,
            'category': project.category,
            'client': project.client,
            'completion_date': project.completion_date,
            'technologies': project.technologies,
            'website': project.website
        })
    return project_list

@login_required(login_url='/accounts/login/')
def about(request):
    db_team_members = TeamMember.objects.all()
    team_members = []
    for member in db_team_members:
        team_members.append({
            'name': member.name,
            'role': member.role,
            'bio': member.bio,
            'image': member.image.url if member.image else '',
            'education': member.education.split('\n') if member.education else [],
            'experience': member.experience.split('\n') if member.experience else [],
            'skills': [skill.strip() for skill in member.skills.split(',')] if member.skills else []
        })
    return render(request, 'core/about.html', {'section': 'about', 'team_members': team_members})

@login_required(login_url='/accounts/login/')
def services(request):
    return render(request, 'core/services.html', {'section': 'services'})

def get_fallback_image(project_title):
    """Returns appropriate placeholder image path based on project title keywords"""
    # For testing purposes, we'll use online images instead of local SVGs
    title = project_title.lower()
    
    if 'e-commerce' in title or 'ecommerce' in title:
        return 'https://via.placeholder.com/800x500/3498db/ffffff?text=E-Commerce+Platform'
    elif 'mobile' in title or 'app' in title or 'fit' in title:
        return 'https://via.placeholder.com/800x500/e74c3c/ffffff?text=Mobile+App+UI'
    elif 'brand' in title or 'techn' in title:
        return 'https://via.placeholder.com/800x500/9b59b6/ffffff?text=Brand+Identity'
    elif 'crm' in title or 'client' in title:
        return 'https://via.placeholder.com/800x500/34495e/ffffff?text=CRM+System'
    elif 'travel' in title or 'eco' in title:
        return 'https://via.placeholder.com/800x500/2ecc71/ffffff?text=Travel+Platform'
    elif 'finance' in title or 'fin' in title:
        return 'https://via.placeholder.com/800x500/f1c40f/ffffff?text=Finance+App'
    elif 'cafe' in title or 'artisan' in title:
        return 'https://via.placeholder.com/800x500/e67e22/ffffff?text=Cafe+Branding'
    elif 'health' in title or 'medi' in title:
        return 'https://via.placeholder.com/800x500/1abc9c/ffffff?text=Healthcare+Portal'
    elif 'blog' in title:
        return 'https://via.placeholder.com/800x500/95a5a6/ffffff?text=News+Blog'
    elif 'corporate' in title or 'edu' in title or 'learn' in title:
        return 'https://via.placeholder.com/800x500/3498db/ffffff?text=Learning+Platform'
    else:
        return 'https://via.placeholder.com/800x500/7f8c8d/ffffff?text=Project+Placeholder'

@login_required(login_url='/accounts/login/')
def portfolio(request):
    projects = get_portfolio_projects()
    
    # Get team members data for the portfolio page
    db_team_members = TeamMember.objects.all()
    team_members = []
    for member in db_team_members:
        # Use member image if available, otherwise use default
        member_image = member.image.url if member.image else '/static/images/default-user.jpg'
        team_members.append({
            'name': member.name,
            'slug': member.slug,
            'email': member.email,
            'role': member.role,
            'bio': member.bio,
            'image': member_image,
        })
    
    return render(request, 'core/portfolio.html', {
        'section': 'portfolio', 
        'projects': projects,
        'team_members': team_members
    })

@login_required(login_url='/accounts/login/')
def contact(request):
    selected_member = None
    member_slug = request.GET.get('member')
    
    # Try to fetch the selected member if slug is provided
    if member_slug:
        try:
            selected_member = TeamMember.objects.get(slug=member_slug)
        except TeamMember.DoesNotExist:
            selected_member = None
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Get team member's email if specified, otherwise use Akash's email
            recipient_email = 'akashcse018@gmail.com'  # Default to Akash's email
            
            # If a team member is specified, route to their email
            if contact_message.team_member:
                try:
                    team_member_obj = TeamMember.objects.get(name=contact_message.team_member)
                    if team_member_obj.email:
                        recipient_email = team_member_obj.email
                except TeamMember.DoesNotExist:
                    pass
            
            # Send email notification
            send_mail(
                f'New Contact Form Submission: {contact_message.subject}',
                f'Name: {contact_message.name}\n'
                f'Email: {contact_message.email}\n'
                f'Team Member: {contact_message.team_member or "Not specified"}\n'
                f'Department: {contact_message.get_department_display() or "Not specified"}\n'
                f'Inquiry Type: {contact_message.get_inquiry_type_display()}\n'
                f'Message: {contact_message.message}',
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect(reverse('contact'))
    else:
        initial_data = {}
        
        # If a team member is selected, pre-fill the subject and team_member fields
        if selected_member:
            initial_data['team_member'] = selected_member.name
            initial_data['subject'] = f'Message for {selected_member.name}'
        
        form = ContactForm(initial=initial_data)
    
    return render(request, 'core/contact.html', {
        'section': 'contact',
        'form': form,
        'selected_member': selected_member
    })

@csrf_exempt
@require_POST
def schedule_meeting(request):
    """AJAX view to handle meeting scheduling - allows unauthenticated users to request meetings"""
    logger = logging.getLogger(__name__)
    try:
        data = json.loads(request.body)
        form = MeetingForm(data)

        logger.info(f"Received meeting request: {data}")
        if not form.is_valid():
            logger.error(f"Form errors: {form.errors}")
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })

        if form.is_valid():
            # Save the meeting to the database
            meeting = form.save(commit=False)
            
            # Generate Google Meet URL
            from .meeting_utils import generate_google_meet_url
            meet_result = generate_google_meet_url(
                meeting_title=meeting.topic,
                meeting_date=meeting.date,
                meeting_time=meeting.time,
                meeting_email=meeting.email,
                meeting_notes=meeting.notes
            )
            
            # Store the Google Calendar event link
            if meet_result.get('success') or meet_result.get('url'):
                meeting.google_meet_url = meet_result.get('url')
                logger.info(f"Google Calendar event created: {meet_result.get('event_id')}")
                logger.info(f"Event link: {meet_result.get('url')}")
            else:
                logger.warning(f"Failed to create calendar event: {meet_result.get('error')}")
            
            # Now save the meeting with the URL
            meeting.save()
            logger.info(f"Meeting saved to database with ID: {meeting.id}")

            # Email to the user (meeting requester)
            user_email_body = f"""
Hello {meeting.name},

Thank you for requesting a meeting with us! We've received your meeting request and will get back to you shortly.

Meeting Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic: {meeting.topic}
Requested Date: {meeting.date.strftime('%A, %B %d, %Y')}
Requested Time: {meeting.time.strftime('%I:%M %p')} IST
Your Email: {meeting.email}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Event Link: {meeting.google_meet_url if meeting.google_meet_url else 'Will be sent after confirmation'}

Additional Notes: {meeting.notes if meeting.notes else 'None provided'}

You will receive a calendar invitation with the Google Meet link shortly. 
You can also use the link above to access the meeting details in Google Calendar.

Best regards,
Serendipity Team
            """

            # Email to admins
            admin_email_body = f"""
New Meeting Request Received!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Requester Name: {meeting.name}
Requester Email: {meeting.email}
Meeting Topic: {meeting.topic}
Requested Date: {meeting.date.strftime('%A, %B %d, %Y')}
Requested Time: {meeting.time.strftime('%I:%M %p')} IST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Calendar Event Link: {meeting.google_meet_url if meeting.google_meet_url else 'Creating event...'}

Additional Notes:
{meeting.notes if meeting.notes else 'None provided'}

The calendar event has been automatically created and is in your Google Calendar.
You can access it via the link above to add a Google Meet call or reschedule if needed.

Action Required:
1. Review the meeting request
2. Accept/Confirm the calendar invitation in your Google Calendar
3. Optional: Add Google Meet conference to the event if not already present
4. Send confirmation to {meeting.email}

You can manage this request in the admin panel.
            """

            # Send confirmation email to user
            try:
                send_mail(
                    f'Meeting Request Received: {meeting.topic}',
                    user_email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [meeting.email],
                    fail_silently=False,
                )
                logger.info(f"User confirmation email sent to {meeting.email}")
            except Exception as email_error:
                logger.warning(f"Failed to send user confirmation email: {str(email_error)}")

            # Send notification email to all admin/superusers
            try:
                from django.contrib.auth.models import User
                admin_emails = User.objects.filter(is_superuser=True).values_list('email', flat=True)
                
                if admin_emails:
                    send_mail(
                        f'New Meeting Request: {meeting.topic}',
                        admin_email_body,
                        settings.DEFAULT_FROM_EMAIL,
                        list(admin_emails),
                        fail_silently=False,
                    )
                    logger.info(f"Admin notification emails sent to {len(admin_emails)} admin(s)")
            except Exception as email_error:
                logger.warning(f"Failed to send admin notification emails: {str(email_error)}")

            return JsonResponse({
                'success': True,
                'message': 'Meeting request submitted successfully! We\'ll send you a confirmation email with the Google Meet link shortly.',
                'meeting_id': meeting.id,
                'meet_url': meeting.google_meet_url,
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })

    except json.JSONDecodeError as e:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data received.'
        })
    except Exception as e:
        # Log the actual error for debugging
        logger.error(f"Error scheduling meeting: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while scheduling the meeting. Please try again.'
        })

@staff_member_required
def meetings(request):
    """Admin view to display all scheduled meetings"""
    meetings_list = Meeting.objects.all().order_by('-created_at')
    return render(request, 'core/meetings.html', {'meetings': meetings_list})

@staff_member_required
def edit_profile(request):
    """Allow admin to edit their own team member profile"""
    # Try to find the team member profile associated with this admin's email
    admin_email = request.user.email
    
    try:
        team_member = TeamMember.objects.get(admin_email=admin_email)
    except TeamMember.DoesNotExist:
        messages.error(request, 'Your profile has not been set up yet. Please contact the site administrator.')
        return redirect('home')
    
    if request.method == 'POST':
        form = TeamMemberEditForm(request.POST, request.FILES, instance=team_member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('edit_profile')
    else:
        form = TeamMemberEditForm(instance=team_member)
    
    return render(request, 'core/edit_profile.html', {
        'form': form,
        'team_member': team_member,
        'section': 'profile'
    })

