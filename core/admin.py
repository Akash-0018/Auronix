from django.contrib import admin
from .models import ContactMessage, Project, TeamMember, Testimonial

# Customize the admin site
admin.site.site_header = "Auronix  Admin"
admin.site.site_title = "Auronix  Admin Portal"
admin.site.index_title = "Welcome to Auronix  Admin"

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'inquiry_type', 'preferred_contact', 'received_at')
    list_filter = ('inquiry_type', 'preferred_contact', 'received_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('received_at',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client', 'completion_date')
    list_filter = ('category', 'completion_date')
    search_fields = ('title', 'description', 'client', 'technologies')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'client', 'completion_date')
        }),
        ('Project Images', {
            'fields': ('image', 'fallback_image', 'external_image'),
            'description': 'Upload project images from your local computer. The external_image flag is for reference only.'
        }),
        ('Additional Details', {
            'fields': ('technologies', 'website', 'team_member'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'admin_email', 'phone', 'role', 'location')
    search_fields = ('name', 'email', 'admin_email', 'role', 'bio', 'skills')
    readonly_fields = ('slug',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'role', 'bio', 'image')
        }),
        ('Contact Details', {
            'fields': ('email', 'phone', 'location'),
            'description': 'These details will appear on the Contact page when users select this team member.'
        }),
        ('Admin Information', {
            'fields': ('admin_email',),
            'description': 'Email of the admin who manages this profile (used as unique identifier).'
        }),
        ('Professional Information', {
            'fields': ('education', 'experience', 'skills'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'workplace', 'feedback')
    search_fields = ('name', 'workplace', 'feedback')
