from django import forms
from django.forms.widgets import SelectDateWidget
from .models import ContactMessage, Project, TeamMember, Meeting

class ContactForm(forms.ModelForm):
    TEAM_CHOICES = [
        ('web', 'Web Development'),
        ('data', 'Data Analytics'),
        ('mobile', 'Mobile App Development'),
        ('social', 'Social Media'),
    ]

    team_member = forms.ChoiceField(
        choices=[
            ('Akash', 'Akash (Web Developer)'),
            ('Bhargavi', 'Bhargavi (Web Developer)'),
            ('Sheik Mathar', 'Sheik Mathar (Data Analyst)'),
            ('Gnanajyothi', 'Gnanajyothi (Mobile App Developer)'),
            ('Praveen', 'Praveen (Social Media Manager)'),
            ('Sanjeev', 'Sanjeev (Social Media Specialist)'),           
            
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Contact Team Member (optional)'
    )

    department = forms.ChoiceField(
        choices=TEAM_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Department (optional)'
    )
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message', 'inquiry_type', 'pricing_plan', 'preferred_contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
            'inquiry_type': forms.Select(attrs={'class': 'form-select'}),
            'pricing_plan': forms.Select(attrs={'class': 'form-select'}),
            'preferred_contact': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'preferred_contact': 'Which email would you like me to respond to?',
            'pricing_plan': 'Selected Pricing Plan'
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'category', 'client', 'completion_date', 'technologies', 'website']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'completion_date': SelectDateWidget(years=range(2000, 2031), attrs={'class': 'form-select d-inline w-auto'}),
            'technologies': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'bio', 'image', 'education', 'experience', 'skills']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class TeamMemberEditForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'email', 'phone', 'role', 'bio', 'image', 'education', 'experience', 'skills', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Role'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Bio'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Education (one per line)'}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Experience (one per line)'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Skills (comma-separated)'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
        }

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['name', 'email', 'topic', 'notes', 'date', 'time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Meeting Topic'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional Notes', 'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'meetingDatePicker', 'autocomplete': 'off'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
