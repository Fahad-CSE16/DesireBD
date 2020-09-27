from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.text import slugify
from PIL import Image
from multiselectfield import MultiSelectField
from person.models import District, SubDistrict, Subject, Classes
# Create your models here.


class TuitionPost(models.Model):
    Choice_Medium = (
        ('Bangla_Medium', 'Bangla Medium'),
        ('English_Medium', 'English Medium'),
        ('Arabic_Medium', 'Arabic Medium'),
        ('Hindi_Medium', 'Hindi Medium'),
        ('Sports_Section', 'Sports Section'),
        ('Singing_Section', 'Singing Section'),
        ('Dance_Section', 'Dance Section'),
        ('Extra Curricular Activities', 'Extra Curricular Activities'),
        ('Language Learning', 'Language Learning'),
        ('Computer Learning', 'Computer Learning'),
    )
    Choice_Approach = (
        ('Online_Help', 'Online Help'),
        ('Phone_Help', 'Phone Help'),
        ('Provide_Hand_Notes', 'Provide Hand_Notes'),
        ('Video_Tutorials', 'Video Tutorials'),
    )
    Choice_style = (
        ('Group_Tuition', 'Group Tuition'),
        ('Private_Tuition', 'Private Tuition'),
    )
    Choice_Place = (
        ('Class_Rooms', 'Class Rooms'),
        ('Coaching_Center', 'Coaching Center'),
        ('Students Home', 'Students Home'),
        ('Teachers Place', 'Teachers Place'),
    )
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, related_name='district_set')
    preferedPlace = models.ManyToManyField(SubDistrict, related_name='place_set')
    style = MultiSelectField(choices=Choice_style, max_choices=4, max_length=100)
    place = MultiSelectField(choices=Choice_Place, max_choices=4, max_length=100)
    approach = MultiSelectField(choices=Choice_Approach,max_choices=4, max_length=100)
    medium = MultiSelectField(choices=Choice_Medium,max_choices=10, max_length=200)
    sno = models.AutoField(primary_key=True)
    subject = models.ManyToManyField(Subject, related_name='subject_set')
    class_in = models.ManyToManyField(Classes, related_name='classes_set')
    salary = models.CharField(max_length=100)
    days=models.CharField(max_length=100)
    time_available = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.ManyToManyField(User, related_name='post_view')
    likes = models.ManyToManyField(User,related_name='tuition_post')
    timeStamp = models.DateTimeField(default=now)
    def total_likes(self):
        return self.likes.count()
    def total_views(self):
        return self.views.count()
    def __str__(self):
        return str(self.sno )+" . "+  self.author.username + " 's Post for searching  a techer in " + str(self.district.name)

    # class Meta:
    #     ordering = ['timeStamp']
        # verbose_name_plural= "Categories"


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tuitionpost = models.ForeignKey(TuitionPost, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='posts/images', default="default.jpg")
    timestamp = models.DateTimeField(default=now)

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.user.username + ": " + self.comment[0:13]

    # class Meta:
    #     ordering = ['timestamp']
        # verbose_name_plural= "Categories"
