from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.text import slugify
from PIL import Image
# Create your models here.


class TuitionPost(models.Model):
    CATEGORY = (
        ('s', 'student'),
        ('t', 'teacher'),
    )
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=255, default=title)
    content = models.TextField()
    views = models.ManyToManyField(User, related_name='post_view')
    likes=models.ManyToManyField(User,related_name='tuition_post')
    timeStamp = models.DateTimeField(default=now)
    category = models.CharField(max_length=1, choices=CATEGORY)
    time_available = models.CharField(max_length=200)
    image = models.ImageField(upload_to='posts/images', default="default.jpg")
    def total_likes(self):
        return self.likes.count()

    def total_views(self):
        return self.views.count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(TuitionPost, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.slug
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
