from django import forms
from django.forms import ModelForm
from . models import District,Places,PersonProfile


class PersonProfileForm(forms.ModelForm):
    class Meta:
        model = PersonProfile
        fields = ('country', 'city')
        widgets = {
            'city': forms.CheckboxSelectMultiple(attrs={'multiple': True})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = Places.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = Places.objects.filter(
                    country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.places_set.order_by(
                'name')
