# Generated by Django 4.2.4 on 2023-09-17 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_enrollment'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
