# Generated by Django 5.0.4 on 2024-04-11 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0026_departments'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='salary',
            field=models.IntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='salary',
        ),
    ]