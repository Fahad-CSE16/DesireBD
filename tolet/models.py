from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from PIL import Image
from django.utils.timezone import now
from person.models import District, SubDistrict
# from main.models import Store

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
    # CATEGORY=(
    #     ('Bill_board', 'Bill_board'),
    #     ('Commercial Space', 'Commercial Space'),
    #     ('Flat/Apartment', 'Flat/Apartment'),
    #     ('Garage', 'Garage'),
    #     ('House', 'House'),
    #     ('Land', 'Land'),
    #     ('Media_advertisement', 'Media_advertisement'),
    #     ('Mess/Hostel_seat', 'Mess/Hostel_seat'),
    #     ('Office', 'Office'),
    #     ('Room', 'Room'),
    #     ('Shop', 'Shop'),
    #     ('Sublet', 'Sublet'),
    # )
class Area(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feeds')
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='districts_set')
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_set')
    area=models.CharField(max_length=300)    
    location=models.CharField(max_length=500)
    rent=models.IntegerField()
    details=models.TextField(blank=False, max_length=500)
    timestamp=models.DateTimeField(default=now)
    views = models.ManyToManyField(User, related_name='tpost_view')
    likes = models.ManyToManyField(User, related_name='tolet_post')

    # class Meta:
    #     ordering = ['timestamp']
        # verbose_name_plural= "Categories"
    def total_likes(self):
        return self.likes.count()

    def total_views(self):
        return self.views.count() 
    
class PostFile(models.Model):
    file = models.ImageField(upload_to="tolet/images")
    feed = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='files')
    def save( self, *args, **kwargs):
        super(PostFile, self).save(*args, **kwargs)
        img = Image.open(self.file.path)

        if img.height > 300 or img.width > 300 :
            output_size =(300, 300)
            img.thumbnail(output_size)
            img.save(self.file.path)

class ToletComment(models.Model):
    sno=models.AutoField(primary_key = True)
    comment=models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null= True)
    image=models.ImageField(upload_to='tolet/images', default="default.jpg")
    timestamp=models.DateTimeField(default= now)
    # class Meta:
    #     ordering = ['timestamp']
        # verbose_name_plural= "Categories"
        
    def save( self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300 :
            output_size =(300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.user.username + ": " +self.comment[0:13] 

