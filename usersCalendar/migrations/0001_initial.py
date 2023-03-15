# Generated by Django 4.1.7 on 2023-03-15 07:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('idols', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(default='', max_length=50)),
                ('contents', models.TextField(blank=True, default='', max_length=500, null=True)),
                ('when', models.DateTimeField(blank=True, null=True)),
                ('owner', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('pick', models.ManyToManyField(to='idols.idol')),
            ],
            options={
                'verbose_name_plural': "User's Calendar",
            },
        ),
    ]
