# Generated by Django 4.2.4 on 2024-03-21 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_assignments_uploadassignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignments',
            name='allowed_file_type',
            field=models.CharField(choices=[('pdf', 'PDF'), ('mp3', 'MP3'), ('mp4', 'MP4')], default=1, max_length=3),
            preserve_default=False,
        ),
    ]
