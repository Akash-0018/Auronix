from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm, TeamMemberEditForm
from django.urls import reverse
from .models import Project, TeamMember
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
        main_image_url = project.image.url if project.image else ''
        # Get fallback image URL (for card preview)
        fallback_image_url = project.fallback_image.url if project.fallback_image else 'https://via.placeholder.com/800x500/7f8c8d/ffffff?text=Project+Placeholder'
        
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
            'image': member.image.url if member.image else 'images/default-user.jpg',
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
        team_members.append({
            'name': member.name,
            'email': member.email,
            'role': member.role,
            'bio': member.bio,
            'image': member.image,
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
    
    # Try to fetch the selected member if slug is provided (for context display only)
    if member_slug:
        try:
            selected_member = TeamMember.objects.get(slug=member_slug)
        except TeamMember.DoesNotExist:
            selected_member = None
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send all emails to the single admin email address
            admin_email = settings.EMAIL_HOST_USER
            
            # Send email notification to admin
            send_mail(
                f'New Contact Form Submission: {contact_message.subject}',
                f'Name: {contact_message.name}\n'
                f'Email: {contact_message.email}\n'
                f'Subject: {contact_message.subject}\n'
                f'Team Member: {contact_message.team_member or "Not specified"}\n'
                f'Department: {contact_message.get_department_display() or "Not specified"}\n'
                f'Inquiry Type: {contact_message.get_inquiry_type_display()}\n'
                f'Preferred Contact: {contact_message.get_preferred_contact_display()}\n'
                f'Pricing Plan: {contact_message.get_pricing_plan_display() if contact_message.pricing_plan else "Not specified"}\n\n'
                f'Message:\n{contact_message.message}',
                settings.DEFAULT_FROM_EMAIL,
                [admin_email],
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect(reverse('contact'))
    else:
        initial_data = {}
        
        # If a team member is selected, pre-fill the subject and team_member fields (optional context)
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
    """AJAX view to handle meeting scheduling - DEPRECATED - Feature removed"""
    return JsonResponse({
        'success': False,
        'message': 'Meeting scheduler has been removed. Please contact us directly.'
    })

@staff_member_required
def meetings(request):
    """Admin view to display all scheduled meetings - DEPRECATED - Feature removed"""
    return render(request, 'core/contact.html', {
        'section': 'contact',
        'message': 'Meeting scheduler has been removed.'
    })



@staff_member_required
def edit_profile(request):
    """Allow admin to edit their own team member profile"""
    # Try to find the team member profile associated with this admin's email
    admin_email = request.user.email
    
    try:
        team_member = TeamMember.objects.get(admin_email=admin_email)
    except TeamMember.DoesNotExist:
        # If profile doesn't exist, create a new one with admin's username/email
        team_member = TeamMember(
            admin_email=admin_email,
            name=request.user.first_name or request.user.username,
            email=admin_email
        )
    
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

