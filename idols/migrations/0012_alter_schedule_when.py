# Generated by Django 4.1.7 on 2023-03-24 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idols', '0011_alter_schedule_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='when',
            field=models.DateTimeField(),
        ),
    ]