# Generated by Django 5.1.2 on 2024-11-13 07:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_reservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='reservationdate',
        ),
        migrations.RemoveField(
            model_name='user',
            name='reservationtime',
        ),
        migrations.RemoveField(
            model_name='user',
            name='tablenumber',
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservedBy',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.user'),
        ),
        migrations.CreateModel(
            name='Makes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservationStatus', models.CharField(choices=[('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Confirmed', max_length=100)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.reservation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.user')),
            ],
            options={
                'unique_together': {('user', 'reservation')},
            },
        ),
    ]
