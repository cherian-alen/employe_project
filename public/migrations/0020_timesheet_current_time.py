# Generated by Django 5.0.2 on 2024-04-10 04:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0019_register_registrationid'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='current_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
