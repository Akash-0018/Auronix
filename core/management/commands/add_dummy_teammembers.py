from django.core.management.base import BaseCommand
from core.models import TeamMember

class Command(BaseCommand):
    help = 'Add dummy team members with given names and emails'

    def handle(self, *args, **kwargs):
        members = {
            'Akash': 'akashcse018@gmail.com',
            'Bhargavi': 'rbhargavi846@gmail.com',
            'Sheik Mathar': 'sheik Mathar@example.com',
            'Gnanajothi': 'gnanajothi@example.com',
            'Praveen': 'praveen@example.com',
            'Sanjeev': 'sanjeev@example.com'
        }

        for name, email in members.items():
            obj, created = TeamMember.objects.get_or_create(
                name=name,
                defaults={
                    'email': email,
                    'role': 'Team Member',
                    'bio': 'This is a dummy bio for ' + name,
                    'education': '',
                    'experience': '',
                    'skills': ''
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Team member "{name}" added.'))
            else:
                self.stdout.write(f'Team member "{name}" already exists.')
