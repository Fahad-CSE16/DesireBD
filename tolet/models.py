from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from PIL import Image
from django.utils.timezone import now
# from main.models import Store

# Create your models here.
class Post(models.Model):
    CATEGORY=(
        ('a', 'Flat'),
        ('b', 'Room'),
        ('c', 'Any_space'),
        ('d', 'Land'),
        ('e', 'Shop'),
        ('f', 'Hostel_seat'),
        ('g', 'Company'),
        ('h', 'Building'),
        ('i', 'Bill_board'),
        ('j', 'Media_advertisement'),
    )
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='feeds')
    house_no=models.CharField(max_length=40, default="")
    post_code=models.CharField(max_length=50, default="")
    road_no=models.CharField(max_length=50, default="")
    village=models.CharField(max_length=50, default="")
    upozila=models.CharField(max_length=50, default="")
    Zilla=models.CharField(max_length=50, default="")
    division=models.CharField(max_length=50, default="")
    country=models.CharField(max_length=50, default="")
    category=models.CharField(max_length=1,choices=CATEGORY, default="")
    rent=models.IntegerField()
    no_of_img=models.IntegerField(default=0)
    area=models.CharField(max_length=50, default="")
    text=models.TextField(blank=False, max_length=500)
    timestamp=models.DateTimeField(default=now)
    views = models.ManyToManyField(User, related_name='tpost_view')
    likes = models.ManyToManyField(User, related_name='tolet_post')

    def total_likes(self):
        return self.likes.count()

    def total_views(self):
        return self.views.count()
    
    def __str__(self):
        return  self.house_no + " " + self.road_no  + " " + self.village + " " + self.area
    

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
    def save( self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300 :
            output_size =(300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.user.username + ": " +self.comment[0:13] 
