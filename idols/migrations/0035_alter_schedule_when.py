# Generated by Django 4.1.7 on 2023-03-11 06:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idols', '0034_alter_schedule_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='when',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 11, 6, 23, 15, 710121, tzinfo=datetime.timezone.utc)),
        ),
    ]
