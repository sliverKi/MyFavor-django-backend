# Generated by Django 4.1.7 on 2023-03-19 06:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idols', '0009_alter_schedule_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='when',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 19, 6, 15, 47, 47625, tzinfo=datetime.timezone.utc)),
        ),
    ]
