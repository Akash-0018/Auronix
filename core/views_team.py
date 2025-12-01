from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import TeamMember, Project
from .forms import ContactForm

def get_team_members():
    """Returns list of all team members with their details"""
    # Use hardcoded data for now to ensure team page displays content
    team_members = [
    ]

    # Try to get additional team members from database if they exist
    try:
        db_members = TeamMember.objects.all()
        for member in db_members:
            # Skip if already in hardcoded list
            if not any(m['name'] == member.name for m in team_members):
                member_dict = {
                    'name': member.name,
                    'email': member.email,
                    'role': member.role,
                    'bio': member.bio,
                    'image': member.image.url if member.image else 'images/profile.jpg',
                    'education': member.education.split('\n') if member.education else [],
                    'experience': member.experience.split('\n') if member.experience else [],
                    'skills': member.skills.split(',') if member.skills else [],
                    'projects': Project.objects.filter(team_member=member),
                    'department': 'web'
                }
                team_members.append(member_dict)
    except:
        # If database query fails, just use hardcoded data
        pass

    return team_members
def team(request):
    """Display all team members"""
    team_members = get_team_members()
    return render(request, 'core/team.html', {'section': 'team', 'team_members': team_members})

def team_member_portfolio(request, member_name):
    """Display individual team member portfolio"""
    try:
        # Get the team member directly from the database
        member = TeamMember.objects.get(name__iexact=member_name.replace('-', ' '))
    except TeamMember.DoesNotExist:
        return redirect('team')
    
    # Get the projects and process their technologies
    projects = Project.objects.filter(team_member=member)
    processed_projects = []
    for project in projects:
        # Handle technologies field - it could be JSON list or comma-separated string
        technologies = project.technologies
        if isinstance(technologies, str):
            technologies = [tech.strip() for tech in technologies.split(',') if tech.strip()]
        elif not isinstance(technologies, list):
            technologies = []

        # Get proper image URLs
        main_image_url = project.image.url if project.image else ''
        fallback_image_url = project.fallback_image.url if project.fallback_image else ''

        project_data = {
            'title': project.title,
            'description': project.description,
            'image': main_image_url,
            'fallback_image': fallback_image_url,
            'image_obj': project.image,
            'category': project.category,
            'get_category_display': project.get_category_display(),
            'client': project.client,
            'completion_date': project.completion_date,
            'website': project.website,
            'technologies': technologies
        }
        processed_projects.append(project_data)
    
    # Prepare member data - ensure image URL is properly set
    member_image_url = member.image.url if member.image else ''
    
    member_data = {
        'name': member.name,
        'slug': member.slug,
        'email': member.email,
        'admin_email': member.admin_email,
        'role': member.role,
        'bio': member.bio,
        'image': member_image_url,
        'image_obj': member.image,
        'location': member.location,
        'phone': member.phone,
        'education': member.education.split('\n') if member.education else [],
        'experience': member.experience.split('\n') if member.experience else [],
        'skills': [skill.strip() for skill in member.skills.split(',') if skill.strip()],
        'projects': processed_projects,
        'testimonials': [
            {
                'text': 'Exceptional work! Their expertise and dedication made our project a huge success.',
                'author': 'John Smith',
                'company': 'TechCorp Solutions'
            },
            {
                'text': 'Brilliant problem-solver and a pleasure to work with. Delivered above and beyond expectations.',
                'author': 'Sarah Johnson',
                'company': 'Digital Innovations Ltd'
            }
        ],
        'certifications': [
            'AWS Certified Solutions Architect',
            'Google Cloud Professional Developer',
            'Microsoft Certified: Azure Developer Associate'
        ] if member.name == 'Akash' else [
            'UI/UX Design Professional Certificate',
            'Adobe Certified Expert',
            'Google UX Design Certificate'
        ] if member.name == 'Bhargavi' else []
    }
    
    return render(request, 'core/team_member_portfolio.html', {
        'section': 'team',
        'member': member_data
    })

def developer_contact(request, member_slug):
    """Display contact form for specific developer"""
    try:
        member = TeamMember.objects.get(slug=member_slug)
    except TeamMember.DoesNotExist:
        return redirect('contact')
    
    member_data = {
        'name': member.name,
        'slug': member.slug,
        'email': member.email,
        'role': member.role,
        'image': member.image.url if member.image else '',
        'location': member.location,
        'phone': member.phone,
    }
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.team_member = member.name
            contact_message.save()
            
            # Send email to developer
            recipient_email = member.email if member.email else 'akashcse018@gmail.com'
            subject = f"New Contact Form Submission: {form.cleaned_data['subject']}"
            message = f"""Hello {member.name},

You have received a new message from {form.cleaned_data['name']}:

Email: {form.cleaned_data['email']}
Subject: {form.cleaned_data['subject']}
Inquiry Type: {form.cleaned_data['inquiry_type']}
Pricing Plan: {form.cleaned_data['pricing_plan']}

Message:
{form.cleaned_data['message']}

---
This message was sent via your portfolio contact form."""
            
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])
            except Exception as e:
                print(f"Error sending email: {e}")
            
            messages.success(request, f'Your message has been sent to {member.name} successfully!')
            return redirect('developer_contact', member_slug=member_slug)
    else:
        form = ContactForm()
    
    return render(request, 'core/developer_contact.html', {
        'form': form,
        'member': member_data,
        'member_data': member_data,
    })
