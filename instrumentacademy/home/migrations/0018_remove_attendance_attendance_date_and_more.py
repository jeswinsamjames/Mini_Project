# Generated by Django 4.2.4 on 2023-10-11 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_attendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='attendance_date',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='is_present',
            field=models.BooleanField(),
        ),
    ]
