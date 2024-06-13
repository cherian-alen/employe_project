# Generated by Django 5.0.2 on 2024-04-09 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0011_complaints'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timesheet',
            name='project',
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.IntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='subtasks',
        ),
    ]
