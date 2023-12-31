# Generated by Django 4.2.4 on 2023-09-24 11:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_remove_lessonmaterial_module_delete_module'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessonmaterial',
            name='category',
        ),
        migrations.RemoveField(
            model_name='lessonmaterial',
            name='visibility',
        ),
        migrations.AddField(
            model_name='lessonmaterial',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lessonmaterial',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lessonmaterial',
            name='material_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lessonmaterial',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='home.coursedetail'),
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('module_number', models.PositiveIntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.coursedetail')),
            ],
        ),
        migrations.AddField(
            model_name='lessonmaterial',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='home.module'),
        ),
    ]
