from .models import (Country, Education, Expectaion, Address, Body, Family, Height, Hobby, Language, Occupation, Personal_Info, Profession, Religion, Sir_name, State, Weight
                     )
from django import forms
from django.forms import ModelForm, DateInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from person.fields import ListTextWidget

class BodyForm(ModelForm):
    class Meta:
        model = Body
        exclude=['user']
class FamilyForm(ModelForm):
    class Meta:
        model = Family
        exclude=['user']
class HobbyForm(ModelForm):
    class Meta:
        model = Hobby
        exclude=['user']
class OccupationForm(ModelForm):
    class Meta:
        model = Occupation
        exclude=['user']
class PersonalForm(ModelForm):
    class Meta:
        model = Personal_Info
        exclude=['user']
class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude=['user']
class ExpectaionForm(ModelForm):
    education = forms.CharField(required=True)
    profession = forms.CharField(required=True)
    religion = forms.CharField(required=True)
    min_age = forms.CharField(required=True)
    max_age = forms.CharField(required=True)
    min_height = forms.CharField(required=True)
    max_height = forms.CharField(required=True)
    class Meta:
        model = Expectaion
        exclude = ['user']
    def __init__(self, *args, **kwargs):
        _company_list = kwargs.pop('data_list', None)
        _profession_list = kwargs.pop('a_list', None)
        _religion_list = kwargs.pop('r_list', None)
        _height_list = kwargs.pop('h_list', None)
        _age_list = kwargs.pop('w_list', None)
        super(ExpectaionForm, self).__init__(*args, **kwargs)
        self.fields['education'].widget = ListTextWidget(data_list=_company_list, name='educaion-list')
        self.fields['profession'].widget = ListTextWidget(data_list=_profession_list, name='profession-list')
        self.fields['religion'].widget = ListTextWidget(data_list=_religion_list, name='religion-list')
        self.fields['min_age'].widget = ListTextWidget(data_list=_age_list, name='min_age-list')
        self.fields['max_age'].widget = ListTextWidget(data_list=_age_list, name='max_age-list')
        self.fields['min_height'].widget = ListTextWidget(data_list=_height_list, name='min_height-list')
        self.fields['max_height'].widget = ListTextWidget(data_list=_height_list, name='max_height-list')
