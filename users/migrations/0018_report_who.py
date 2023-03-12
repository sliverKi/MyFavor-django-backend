# Generated by Django 4.1.7 on 2023-03-12 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idols', '0061_alter_schedule_when'),
        ('users', '0017_alter_report_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='who',
            field=models.ManyToManyField(blank=True, null=True, related_name='report', to='idols.idol'),
        ),
    ]