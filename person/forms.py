from django import forms
from django.forms import ModelForm, DateInput
from .models import UserProfile , Contact,SSC,HSC,HigherStudies,AfterHsc,SubDistrict,Subject,District,TuitionClass,Classes
from django.contrib.auth.models import User

class UserUpdateForm(ModelForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields = ['username', 'email', 'first_name', 'last_name']


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields='__all__'
class SSCForm(ModelForm):
    class Meta:
        model = SSC
        exclude = ['user']
        


class HSCForm(ModelForm):
    class Meta:
        model = HSC
        exclude = ['user']


class AfterHscForm(ModelForm):
    class Meta:
        model = AfterHsc
        exclude = ['user']


class HigherStudiesForm(ModelForm):
    class Meta:
        model = HigherStudies
        exclude = ['user']


# class SubDistrictModelForm(forms.ModelForm):
#     class Meta:
#         model = SubDistrict
#         fields = ['name']
        
class TuitionClassForm(ModelForm):
    class Meta:
        model = TuitionClass
        exclude = ['user', 'preferedPlace']
        widgets = {
            'subject': forms.CheckboxSelectMultiple(attrs={'multiple': True}),
            'level': forms.CheckboxSelectMultiple(attrs={'multiple': True}),
            
        }



class TuitionClassUpdateForm(ModelForm):
    class Meta:
        model = TuitionClass
        exclude = ['user']
        widgets = {
            'subject': forms.CheckboxSelectMultiple(attrs={'multiple': True}),
            'level': forms.CheckboxSelectMultiple(attrs={'multiple': True}),
            'preferedPlace': forms.CheckboxSelectMultiple(attrs={'multiple': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['preferedPlace'].queryset = SubDistrict.objects.none()

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['preferedPlace'].queryset = SubDistrict.objects.filter(
                    district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['preferedPlace'].queryset = self.instance.district.subdistrict.order_by('name')

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birth_date','blood_group','genre','address','phone','locatity','religion','marital_status','biodata','category','image']
        # exclude = ['user']
        # fields='__all__'
        widgets = {

            'birth_date': DateInput(attrs={'type': 'date', 'placeholder':'Enter your Birthday'}),
            'user':forms.HiddenInput(),
            'address': forms.TextInput(attrs={ 'placeholder':'Enter your Address'})
            #  'locatity': 
        }

class ContactForm(ModelForm):
    email=forms.EmailField()
    class Meta:
        model=Contact
        fields=['name','email','phone','content']
    
