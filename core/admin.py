from django.contrib import admin
from .models import ContactMessage, Project, TeamMember, Meeting, Testimonial

# Customize the admin site
admin.site.site_header = "Serendipity Admin"
admin.site.site_title = "Serendipity Admin Portal"
admin.site.index_title = "Welcome to Serendipity Admin"

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

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'topic', 'date', 'time', 'status', 'created_at', 'google_meet_url_link')
    list_filter = ('status', 'date', 'created_at')
    search_fields = ('name', 'email', 'topic', 'notes')
    readonly_fields = ('created_at', 'google_meet_url')
    
    fieldsets = (
        ('Meeting Request', {
            'fields': ('name', 'email', 'topic', 'date', 'time', 'notes')
        }),
        ('Meeting Status', {
            'fields': ('status', 'google_meet_url')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['generate_meet_links', 'mark_as_confirmed', 'mark_as_completed']
    
    def google_meet_url_link(self, obj):
        """Display Google Meet URL as clickable link in list view"""
        if obj.google_meet_url:
            return f'<a href="{obj.google_meet_url}" target="_blank" rel="noopener noreferrer">Join Meet</a>'
        return '-'
    google_meet_url_link.short_description = 'Meet Link'
    google_meet_url_link.allow_tags = True
    
    def generate_meet_links(self, request, queryset):
        """Action to generate Google Meet links for selected meetings"""
        from .meeting_utils import generate_google_meet_url
        from django.core.mail import send_mail
        from django.conf import settings
        import logging
        import sys
        
        logger = logging.getLogger(__name__)
        updated_count = 0
        error_count = 0
        
        # Log to see the action is being called
        print("\n" + "="*70)
        print("🎬 ADMIN ACTION: GENERATE MEET LINKS")
        print("="*70)
        print(f"Processing {queryset.count()} meeting(s)")
        sys.stdout.flush()
        
        for meeting in queryset:
            print(f"\n📌 Meeting ID {meeting.id}: {meeting.topic}")
            print(f"   Current URL: {meeting.google_meet_url}")
            print(f"   Status: {meeting.status}")
            sys.stdout.flush()
            
            if not meeting.google_meet_url:
                print(f"   ✓ URL is empty, generating...")
                sys.stdout.flush()
                
                try:
                    print(f"\n📌 Processing Meeting ID {meeting.id}: {meeting.topic}")
                    sys.stdout.flush()
                    
                    # Generate Google Meet URL using OAuth if available
                    result = generate_google_meet_url(
                        meeting_title=meeting.topic,
                        meeting_date=meeting.date,
                        meeting_time=meeting.time,
                        meeting_email=meeting.email,
                        meeting_notes=meeting.notes if meeting.notes else ""
                    )
                    
                    sys.stdout.flush()
                    
                    # Extract URL from result dictionary
                    if isinstance(result, dict):
                        meet_url = result.get('url')
                        method = result.get('method', 'unknown')
                        event_id = result.get('event_id', '')
                        is_real = method == 'calendar_api'
                    else:
                        meet_url = result
                        method = 'unknown'
                        is_real = False
                    
                    if meet_url:
                        meeting.google_meet_url = meet_url
                        meeting.status = 'confirmed'
                        meeting.save()
                        
                        print(f"✅ Saved URL: {meet_url}")
                        print(f"   Method: {method} {'(REAL)' if is_real else '(fallback)'}")
                        sys.stdout.flush()
                        
                        # Log the meeting creation
                        logger.info(f"✓ Meeting {meeting.id} - {meeting.topic}")
                        logger.info(f"  Method: {method} {'(REAL)' if is_real else '(fallback)'}")
                        if event_id:
                            logger.info(f"  Event ID: {event_id}")
                        
                        # Send email to user with Google Meet link
                        email_body = f"""
Hello {meeting.name},

Your meeting has been confirmed! Here are the details:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 Meeting Topic: {meeting.topic}
📆 Date: {meeting.date.strftime('%A, %B %d, %Y')}
🕐 Time: {meeting.time.strftime('%I:%M %p')} UTC
🎥 Google Meet Link: {meet_url}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Join the meeting here: {meet_url}

📝 Additional Notes: {meeting.notes if meeting.notes else 'None'}

We look forward to meeting with you!

Best regards,
Serendipity Team
                        """
                        
                        try:
                            send_mail(
                                f'✓ Meeting Confirmed: {meeting.topic}',
                                email_body,
                                settings.DEFAULT_FROM_EMAIL,
                                [meeting.email],
                                fail_silently=False,
                            )
                            print(f"📧 Email sent to {meeting.email}")
                            logger.info(f"  Email sent to: {meeting.email}")
                            sys.stdout.flush()
                        except Exception as e:
                            logger.error(f"Error sending email to {meeting.email}: {str(e)}")
                            print(f"❌ Email error: {str(e)}")
                            self.message_user(request, f'⚠️ Error sending email to {meeting.email}: {str(e)}')
                            sys.stdout.flush()
                        
                        updated_count += 1
                    else:
                        error_count += 1
                        print(f"❌ No URL generated for meeting {meeting.id}")
                        logger.error(f"Failed to generate URL for meeting {meeting.id}")
                        sys.stdout.flush()
                        
                except Exception as e:
                    error_count += 1
                    print(f"❌ Error: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    logger.error(f"Error processing meeting {meeting.id}: {str(e)}")
                    self.message_user(request, f'❌ Error processing meeting {meeting.id}: {str(e)}')
                    sys.stdout.flush()
            else:
                print(f"   ⏭️ Skipping (already has URL)")
                sys.stdout.flush()
        
        print("\n" + "="*70)
        if updated_count > 0:
            msg = f'✓ Generated and sent Google Meet links for {updated_count} meeting(s).'
            print(msg)
            self.message_user(request, msg)
        if error_count > 0:
            msg = f'❌ Failed to process {error_count} meeting(s). Check logs for details.'
            print(msg)
            self.message_user(request, msg)
        if updated_count == 0 and error_count == 0:
            print("⏭️ No meetings to process (all may already have URLs)")
            self.message_user(request, "✓ All meetings already have Google Meet links")
        print("="*70 + "\n")
        sys.stdout.flush()
    generate_meet_links.short_description = 'Generate Google Meet links and send to users'
    
    def mark_as_confirmed(self, request, queryset):
        """Mark meetings as confirmed"""
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} meeting(s) marked as confirmed.')
    mark_as_confirmed.short_description = 'Mark selected meetings as confirmed'
    
    def mark_as_completed(self, request, queryset):
        """Mark meetings as completed"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} meeting(s) marked as completed.')
    mark_as_completed.short_description = 'Mark selected meetings as completed'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'workplace', 'feedback')
    search_fields = ('name', 'workplace', 'feedback')
