# Generated by Django 5.0.2 on 2024-04-09 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0014_complaints_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.IntegerField(default=0, null=True),
        ),
    ]