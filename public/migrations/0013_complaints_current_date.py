# Generated by Django 5.0.2 on 2024-04-09 08:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0012_remove_timesheet_project_alter_task_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaints',
            name='current_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
