# Generated by Django 4.1.7 on 2023-03-22 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('idols', '0008_alter_idol_idol_name_en_alter_idol_idol_name_kr_and_more'),
        ('media', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='schedule',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='title',
        ),
        migrations.RemoveField(
            model_name='video',
            name='schedule',
        ),
        migrations.AddField(
            model_name='photo',
            name='idol',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='photo', to='idols.idol'),
        ),
    ]
