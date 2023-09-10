# Generated by Django 4.2.4 on 2023-09-09 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_tutor'),
    ]

    operations = [
        migrations.DeleteModel(
            name='tutor_registrationtable',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phoneNo',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='specialist',
            field=models.CharField(blank=True, choices=[('piano', 'Piano'), ('violin', 'Violin'), ('guitar', 'Guitar'), ('other', 'Other')], max_length=50, null=True),
        ),
    ]
