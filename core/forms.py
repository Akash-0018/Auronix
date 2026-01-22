from django import forms
from django.forms.widgets import SelectDateWidget
from .models import ContactMessage, Project, TeamMember

class ContactForm(forms.ModelForm):
    """Contact form - all emails go to admin inbox"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message', 'inquiry_type', 'pricing_plan']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
            'inquiry_type': forms.Select(attrs={'class': 'form-select'}),
            'pricing_plan': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
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

