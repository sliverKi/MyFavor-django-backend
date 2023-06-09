# Generated by Django 4.1.7 on 2023-03-23 15:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Idol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Girl_group', models.CharField(blank=True, choices=[('GirlGroup', 'GirlGroup'), ('BoyGroup', 'BoyGroup')], max_length=40, null=True)),
                ('Boy_group', models.CharField(blank=True, choices=[('GirlGroup', 'GirlGroup'), ('BoyGroup', 'BoyGroup')], max_length=40, null=True)),
                ('idol_solo', models.CharField(blank=True, choices=[('GirlSolo', 'GirlSolo'), ('BoySolo', 'BoySolo')], max_length=40, null=True)),
                ('idol_name_kr', models.CharField(default='', max_length=100)),
                ('idol_name_en', models.CharField(default='', max_length=100)),
                ('idol_profile', models.URLField(blank=True, max_length=10000, null=True)),
                ('idol_anniv', models.DateField(default=datetime.date.today)),
                ('idol_birthday', models.DateField()),
                ('idol_gender', models.CharField(choices=[('Woman', 'Woman'), ('Man', 'Man')], max_length=8)),
            ],
            options={
                'verbose_name_plural': 'Our_Idols',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('ScheduleTitle', models.CharField(default='', max_length=150)),
                ('location', models.CharField(default='', max_length=150)),
                ('when', models.DateTimeField(default=datetime.datetime(2023, 3, 23, 15, 14, 1, 488470))),
                ('ScheduleType', models.ForeignKey(blank=True, max_length=150, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedules', to='categories.category')),
                ('participant', models.ManyToManyField(blank=True, max_length=150, related_name='schedules', to='idols.idol')),
            ],
            options={
                'verbose_name_plural': 'Idol-Schedules',
            },
        ),
        migrations.AddField(
            model_name='idol',
            name='idol_schedules',
            field=models.ManyToManyField(blank=True, related_name='idols', to='idols.schedule'),
        ),
    ]
