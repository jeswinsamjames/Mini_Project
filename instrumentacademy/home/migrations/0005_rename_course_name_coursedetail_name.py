# Generated by Django 4.2.4 on 2023-09-14 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_category_options_coursedetail_course_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursedetail',
            old_name='course_name',
            new_name='name',
        ),
    ]
