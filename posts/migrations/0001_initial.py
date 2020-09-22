# Generated by Django 3.0.8 on 2020-09-22 02:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('person', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TuitionPost',
            fields=[
                ('style', multiselectfield.db.fields.MultiSelectField(choices=[('Group_Tuition', 'Group Tuition'), ('Private_Tuition', 'Private Tuition')], max_length=100)),
                ('place', multiselectfield.db.fields.MultiSelectField(choices=[('Class_Rooms', 'Class Rooms'), ('Coaching_Center', 'Coaching Center'), ('Home_Visit', 'Home Visit')], max_length=100)),
                ('approach', multiselectfield.db.fields.MultiSelectField(choices=[('Online_Help', 'Online Help'), ('Phone_Help', 'Phone Help'), ('Provide_Hand_Notes', 'Provide Hand_Notes'), ('Video_Tutorials', 'Video Tutorials')], max_length=100)),
                ('medium', multiselectfield.db.fields.MultiSelectField(choices=[('Bangla_Medium', 'Bangla Medium'), ('English_Medium', 'English Medium'), ('Arabic_Medium', 'Arabic Medium'), ('Hindi_Medium', 'Hindi Medium'), ('Sports_Section', 'Sports Section'), ('Singing_Section', 'Singing Section'), ('Dance_Section', 'Dance Section'), ('Extra Curricular Activities', 'Extra Curricular Activities'), ('Language Learning', 'Language Learning'), ('Computer Learning', 'Computer Learning')], max_length=100)),
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('salary', models.CharField(max_length=100)),
                ('days', models.CharField(max_length=100)),
                ('time_available', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('timeStamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('class_in', models.ManyToManyField(related_name='classes_set', to='person.Classes')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='district_set', to='person.District')),
                ('likes', models.ManyToManyField(related_name='tuition_post', to=settings.AUTH_USER_MODEL)),
                ('preferedPlace', models.ManyToManyField(related_name='place_set', to='person.SubDistrict')),
                ('subject', models.ManyToManyField(related_name='subject_set', to='person.Subject')),
                ('views', models.ManyToManyField(related_name='post_view', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('image', models.ImageField(default='default.jpg', upload_to='posts/images')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.BlogComment')),
                ('tuitionpost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.TuitionPost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
