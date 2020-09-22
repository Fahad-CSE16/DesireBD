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
    class Meta:
        model = Expectaion
        exclude=['user']