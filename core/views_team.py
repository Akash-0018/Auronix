from django.shortcuts import render, redirect
from .models import TeamMember, Project

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

        project_data = {
            'title': project.title,
            'description': project.description,
            'image': project.image,
            'category': project.category,
            'get_category_display': project.get_category_display(),
            'client': project.client,
            'completion_date': project.completion_date,
            'website': project.website,
            'technologies': technologies
        }
        processed_projects.append(project_data)
    
    # Prepare member data
    member_data = {
        'name': member.name,
        'email': member.email,
        'admin_email': member.admin_email,
        'role': member.role,
        'bio': member.bio,
        'image': member.image,
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
