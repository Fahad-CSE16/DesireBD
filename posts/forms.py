from django import forms
from django.forms import ModelForm, DateInput
from .models import TuitionPost
from person.models import District, SubDistrict
from django.contrib.auth.models import User


class TuitionPostForm(ModelForm):
    class Meta:
        model = TuitionPost
        exclude = ['author', 'preferedPlace', 'sno', 'views', 'likes','timeStamp']
        # fields = ['title', 'content', 'category', 'time_available', 'image']
        widgets = {
            'subject': forms.CheckboxSelectMultiple(attrs={'multiple': True}),
            'class_in': forms.CheckboxSelectMultiple(attrs={'multiple': True}),

        }
class TuitionPostUpdateForm(ModelForm):
    class Meta:
        model = TuitionPost
        exclude = ['author', 'sno', 'district','views', 'likes','timeStamp']
        # fields = ['title', 'content', 'category', 'time_available', 'image']
        widgets = {
            'subject': forms.CheckboxSelectMultiple(attrs={'multiple': True}),
            'class_in': forms.CheckboxSelectMultiple(attrs={'multiple': True}),
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
