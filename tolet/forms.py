from django.forms import ClearableFileInput
from django import forms
from django.forms import ModelForm, DateInput
from .models import Post,PostFile
from django.contrib.auth.models import User
from person.fields import ListTextWidget

class PostModelForm(forms.ModelForm):
    area = forms.CharField(required=True)
    class Meta:
        model = Post
        fields = '__all__'
        exclude=['user','timestamp','views','likes']
        widgets = {
            
            # 'no_of_img': forms.TextInput(attrs={ 'placeholder':'Enter The number of image you want to add(minimum 1)'}),
            'rent': forms.TextInput(attrs={ 'placeholder':'Enter Rent per month'}),
            'details': forms.Textarea(attrs={ 'placeholder':'Say something About your Property!'})
        }
        labels = {
            # 'no_of_img':' Number of Images',
            # 'text':' Your Words'
        }
    def __init__(self, *args, **kwargs):
        _company_list = kwargs.pop('data_list', None)
        super(PostModelForm, self).__init__(*args, **kwargs)
        self.fields['area'].widget = ListTextWidget(data_list=_company_list, name='area-list')

class FileModelForm(forms.ModelForm):
    class Meta:
        model = PostFile
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
           }
        # widget is important to upload multiple files
