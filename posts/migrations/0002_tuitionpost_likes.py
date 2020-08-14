# Generated by Django 3.0.8 on 2020-08-11 11:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tuitionpost',
            name='likes',
            field=models.ManyToManyField(related_name='tuition_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
