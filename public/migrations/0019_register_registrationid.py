# Generated by Django 5.0.2 on 2024-04-09 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0018_leave_date_leave_ltype'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='registrationid',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
