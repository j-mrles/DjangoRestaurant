# Generated by Django 5.1.2 on 2024-11-01 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_user_reservationdate_user_reservationtime_user_role_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='123', max_length=128),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='Admin', max_length=150, unique=True),
        ),
    ]
