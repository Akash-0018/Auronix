"""
Management command to migrate project images to the new folder structure.
Run with: python manage.py migrate_project_images
"""

import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Project


class Command(BaseCommand):
    help = 'Migrates existing project images to the new folder structure (project_images/ and project_fallback_images/)'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        projects_dir = os.path.join(media_root, 'projects')
        
        # Create the new directories if they don't exist
        main_images_dir = os.path.join(projects_dir, 'project_images')
        fallback_images_dir = os.path.join(projects_dir, 'project_fallback_images')
        
        os.makedirs(main_images_dir, exist_ok=True)
        os.makedirs(fallback_images_dir, exist_ok=True)
        
        self.stdout.write(f'Created directories: {main_images_dir}, {fallback_images_dir}')
        
        # Get all projects with images
        projects = Project.objects.exclude(image__isnull=True).exclude(image='')
        
        migrated_count = 0
        
        for project in projects:
            if project.image:
                # Get the image path
                image_path = os.path.join(media_root, str(project.image))
                
                # If the image is still in the old location, move it
                if os.path.exists(image_path) and 'project_images' not in str(project.image):
                    try:
                        filename = os.path.basename(image_path)
                        new_path = os.path.join(main_images_dir, filename)
                        
                        # Handle duplicate filenames
                        counter = 1
                        base, ext = os.path.splitext(filename)
                        while os.path.exists(new_path):
                            new_path = os.path.join(main_images_dir, f'{base}_{counter}{ext}')
                            counter += 1
                        
                        # Move the file
                        shutil.move(image_path, new_path)
                        
                        # Update the database record
                        project.image = f'projects/project_images/{os.path.basename(new_path)}'
                        project.save()
                        
                        migrated_count += 1
                        self.stdout.write(f'✓ Migrated main image for: {project.title}')
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'✗ Failed to migrate image for {project.title}: {str(e)}'))
        
        # Migrate fallback images
        fallback_count = 0
        projects = Project.objects.exclude(fallback_image__isnull=True).exclude(fallback_image='')
        
        for project in projects:
            if project.fallback_image:
                image_path = os.path.join(media_root, str(project.fallback_image))
                
                if os.path.exists(image_path) and 'project_fallback_images' not in str(project.fallback_image):
                    try:
                        filename = os.path.basename(image_path)
                        new_path = os.path.join(fallback_images_dir, filename)
                        
                        # Handle duplicate filenames
                        counter = 1
                        base, ext = os.path.splitext(filename)
                        while os.path.exists(new_path):
                            new_path = os.path.join(fallback_images_dir, f'{base}_{counter}{ext}')
                            counter += 1
                        
                        # Move the file
                        shutil.move(image_path, new_path)
                        
                        # Update the database record
                        project.fallback_image = f'projects/project_fallback_images/{os.path.basename(new_path)}'
                        project.save()
                        
                        fallback_count += 1
                        self.stdout.write(f'✓ Migrated fallback image for: {project.title}')
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'✗ Failed to migrate fallback image for {project.title}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Migration complete!\n   - {migrated_count} main images migrated\n   - {fallback_count} fallback images migrated'))
