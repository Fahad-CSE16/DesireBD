# Generated by Django 3.0.8 on 2020-09-23 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrimony', '0009_auto_20200923_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='personal_info',
            name='highest_degree_of_education',
            field=models.CharField(default='', max_length=30),
        ),
    ]