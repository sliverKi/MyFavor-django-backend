# Generated by Django 4.1.7 on 2023-03-14 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_report_is_correct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='is_correct',
        ),
    ]
