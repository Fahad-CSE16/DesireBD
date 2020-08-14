from django import forms
from django.forms import ModelForm, DateInput
from .models import TuitionPost
from django.contrib.auth.models import User


class TuitionPostForm(ModelForm):
    class Meta:
        model = TuitionPost
        fields = ['title', 'content', 'category', 'time_available', 'image']
       
