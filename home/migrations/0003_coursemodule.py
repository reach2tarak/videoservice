# Generated by Django 3.1.7 on 2021-03-11 16:09

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210311_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_module_name', models.CharField(max_length=100)),
                ('course_description', ckeditor.fields.RichTextField()),
                ('video_ulr', models.URLField(max_length=300)),
                ('can_view', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.course')),
            ],
        ),
    ]