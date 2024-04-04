# Generated by Django 4.2.4 on 2024-04-03 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0038_alter_coursedetail_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursedetail',
            options={},
        ),
        migrations.AddField(
            model_name='ratingreview',
            name='sentiment_score',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
    ]