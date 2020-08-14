from django.forms import ClearableFileInput
from django import forms
from django.forms import ModelForm, DateInput
from .models import Post,PostFile
from django.contrib.auth.models import User
class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude=['user','timestamp','views','likes']
        widgets = {
            
            'no_of_img': forms.TextInput(attrs={ 'lebel':'Say Something','placeholder':'Enter The number of image you want to add(minimum 1)'}),
            'text': forms.Textarea(attrs={ 'lebel':'Say Something','placeholder':'Say something that You want to say about your assets.'})
        }

class FileModelForm(forms.ModelForm):
    class Meta:
        model = PostFile
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
           }
        # widget is important to upload multiple files