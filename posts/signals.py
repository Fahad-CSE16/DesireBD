# # signals.py

# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import TuitionPost


# @receiver(post_save, sender=User)
# def create_post(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# post_save.connect(create_post, sender=User)


# @receiver(post_save, sender=User)
# def save_post(sender, instance, **kwargs):
#     instance.profile.save()
