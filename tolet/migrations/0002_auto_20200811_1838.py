# Generated by Django 3.0.8 on 2020-08-11 12:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tolet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='view',
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='tolet_post', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.ManyToManyField(related_name='tpost_view', to=settings.AUTH_USER_MODEL),
        ),
    ]
