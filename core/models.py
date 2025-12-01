from django.db import models
from django.utils import timezone

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('Web Development', 'Web Development'),
        ('UI/UX Design', 'UI/UX Design'),
        ('Branding', 'Branding'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/project_images/', blank=True, null=True, help_text="Main project image for modal/detail view")
    fallback_image = models.ImageField(upload_to='projects/project_fallback_images/', blank=True, null=True, help_text="Fallback image for project card preview")
    external_image = models.BooleanField(default=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    client = models.CharField(max_length=200)
    completion_date = models.CharField(max_length=50)
    technologies = models.JSONField(default=list)
    website = models.URLField(blank=True, null=True)
    team_member = models.ForeignKey('TeamMember', on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')

    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    admin_email = models.EmailField(unique=True, blank=True, null=True, help_text="Email of the admin who manages this profile")
    phone = models.CharField(max_length=20, blank=True, null=True, help_text="Phone number for contact (e.g., +91 98434 64180)")
    role = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True, help_text="City/Location for this team member (e.g., Coimbatore, TN, India)")
    slug = models.SlugField(unique=True, blank=True, null=True, help_text="URL-friendly identifier (auto-generated from name)")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    workplace = models.CharField(max_length=200)
    feedback = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.workplace}"

class ContactMessage(models.Model):
    INQUIRY_CHOICES = [
        ('general', 'General Inquiry'),
        ('project', 'Project Proposal'),
        ('collaboration', 'Collaboration'),
        ('job', 'Job Opportunity'),
    ]
    DEPARTMENT_CHOICES = [
        ('web', 'Web Development'),
        ('data', 'Data Analytics'),
        ('mobile', 'Mobile App Development'),
        ('social', 'Social Media'),
    ]
    PRICING_PLAN_CHOICES = [
        ('basic', 'Basic - ₹5000'),
        ('professional', 'Professional - ₹8000'),
        ('custom', 'Custom - 9500-11000'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_CHOICES, default='general')
    pricing_plan = models.CharField(max_length=20, choices=PRICING_PLAN_CHOICES, blank=True, null=True)
    received_at = models.DateTimeField(default=timezone.now)
    preferred_contact = models.CharField(
        max_length=50,
        choices=[('email1', 'Business Email'), ('email2', 'Personal Email')],
        default='email1'
    )
    team_member = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, blank=True, null=True)


    def __str__(self):
        return f"{self.name} - {self.subject}"

class Meeting(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending - Awaiting Confirmation'),
        ('confirmed', 'Confirmed - Meet Link Sent'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    topic = models.CharField(max_length=200)
    notes = models.TextField(default='', blank=True)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    google_meet_url = models.URLField(blank=True, null=True, help_text="Google Meet link for this meeting")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Meeting with {self.name} on {self.date} at {self.time}"
