from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class District(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Places(models.Model):
    country = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class PersonProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    city = models.ManyToManyField(Places, related_name='places_set')