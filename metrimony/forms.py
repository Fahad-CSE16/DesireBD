from .models import (Country, Education, Expectaion, Address, Body, Family, Height, Hobby, Language, Occupation, Personal_Info, Profession, Religion, Sir_name, State, Weight
                     )
from django import forms
from django.forms import ModelForm, DateInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from person.fields import ListTextWidget

class BodyForm(ModelForm):
    height=forms.CharField(required=True)
    class Meta:
        model = Body
        exclude = ['user']
    def __init__(self, *args, **kwargs):
        _height_list = kwargs.pop('data_list', None)
        super(BodyForm, self).__init__(*args, **kwargs)
        self.fields['height'].widget = ListTextWidget(data_list=_height_list, name='height-list')
class HobbyForm(ModelForm):
    class Meta:
        model = Hobby
        exclude = ['user']
        

class FamilyForm(ModelForm):
    class Meta:
        model = Family
        exclude = ['user']
    def __init__(self, *args, **kwargs):
        _profession_list = kwargs.pop('data_list', None)
        super(FamilyForm, self).__init__(*args, **kwargs)
        self.fields['fathers_occupation'].widget = ListTextWidget( data_list=_profession_list, name='fathers_occupation-list')
        self.fields['mothers_occupation'].widget = ListTextWidget(data_list=_profession_list, name='mothers_occupation-list')
class OccupationForm(ModelForm):
    class Meta:
        model = Occupation
        exclude = ['user']
    def __init__(self, *args, **kwargs):
        _profession_list = kwargs.pop('data_list', None)
        _company_list = kwargs.pop('c_list', None)
        super(OccupationForm, self).__init__(*args, **kwargs)
        self.fields['occupation'].widget = ListTextWidget( data_list=_profession_list, name='occupation-list')
        self.fields['company'].widget = ListTextWidget( data_list=_company_list, name='company-list')
class PersonalForm(ModelForm):
    birth_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date', 'class': 'form-control'}))
    class Meta:
        model = Personal_Info
        exclude = ['user']
        widgets = {
            'languages': forms.CheckboxSelectMultiple(attrs={'multiple': True}),
            
        }

    def __init__(self, *args, **kwargs):
        _height_list = kwargs.pop('data_list', None)
        _language_list = kwargs.pop('l_list', None)
        _religion_list = kwargs.pop('r_list', None)
        super(PersonalForm, self).__init__(*args, **kwargs)
        self.fields['sir_name'].widget = ListTextWidget( data_list=_height_list, name='sir_name-list')
        self.fields['mother_tongue'].widget = ListTextWidget(data_list=_language_list, name='mother_tongue-list')
        self.fields['religion'].widget = ListTextWidget(data_list=_religion_list, name='religion-list')

class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        _district_list = kwargs.pop('data_list', None)
        _state_list = kwargs.pop('s_list', None)
        _country_list = kwargs.pop('c_list', None)
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['district'].widget = ListTextWidget(
            data_list=_district_list, name='district-list')
        self.fields['state'].widget = ListTextWidget(
            data_list=_state_list, name='state-list')
        self.fields['residency_country'].widget = ListTextWidget(data_list=_country_list, name='residency_country-list')
        self.fields['birth_country'].widget = ListTextWidget(data_list=_country_list, name='birth_country-list')
        self.fields['grow_up_country'].widget = ListTextWidget(data_list=_country_list, name='grow_up_country-list')
        
        
        
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
