from django import forms
from django.forms import ModelForm, DateInput
from .models import UserProfile, Contact, SSC, HSC, HigherStudies, AfterHsc, SubDistrict, Subject, District, TuitionClass, Classes
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email address is already in use.")
        else:
            return email

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     username=self.cleaned_data.get('username')
    #     userp=User.objects.get(username=username)
    #     if User.objects.filter(email=email).exists() and userp.email != email :
    #         raise forms.ValidationError(
    #             "This email address is already in use.")
    #     else:
    #         return email

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'


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
        exclude = ['user', 'district']
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
            self.fields['preferedPlace'].queryset = self.instance.district.subdistrict.order_by(
                'name')

class UserProfileForm(ModelForm):
    # birth_date = forms.DateInput(input_formats=DATE_INPUT_FORMATS)
    # birth_date= forms.DateField(localize=True, widget=forms.DateInput(format='%Y-%m-%D', attrs={'type':'date'}))
    class Meta:
        model = UserProfile
        fields = ['birth_date', 'blood_group', 'genre', 'address', 'phone',
                  'nationality', 'religion', 'marital_status', 'biodata', 'profession', 'image']
        # exclude = ['user']
        # fields='__all__'
        widgets = {

            'birth_date': DateInput(attrs={'type': 'date', format: '%Y-%m-%D', 'placeholder': 'Enter your Birthday'}),
            'user': forms.HiddenInput(),
            'address': forms.TextInput(attrs={'placeholder': 'Enter your Address'})
            #  'locatity':
        }
        label = {
            'genre':'Gender'
        }


class ContactForm(ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'content']
