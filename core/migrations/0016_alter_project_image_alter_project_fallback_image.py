# Generated migration to update project image upload paths

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_meeting_google_meet_url_meeting_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(
                blank=True,
                help_text='Main project image (shown in modal/detail view) - Recommended: 1200x800px',
                null=True,
                upload_to='projects/project_images/'
            ),
        ),
        migrations.AlterField(
            model_name='project',
            name='fallback_image',
            field=models.ImageField(
                blank=True,
                help_text='Fallback image (shown on portfolio page) - Recommended: 400x300px',
                null=True,
                upload_to='projects/project_fallback_images/'
            ),
        ),
    ]
