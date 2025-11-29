from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views_team import team, team_member_portfolio

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('contact/', views.contact, name='contact'),
    path('schedule-meeting/', views.schedule_meeting, name='schedule_meeting'),
    path('meetings/', views.meetings, name='meetings'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('team/', team, name='team'),
    path('team/<str:member_name>/', team_member_portfolio, name='team_member_portfolio'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
