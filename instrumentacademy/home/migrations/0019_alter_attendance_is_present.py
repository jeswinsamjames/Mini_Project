# Generated by Django 4.2.4 on 2023-10-13 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_remove_attendance_attendance_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='is_present',
            field=models.BooleanField(null=True),
        ),
    ]