from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import PersonProfile, District,Places
from . forms import PersonProfileForm
# Create your views here.


class PersonListView(ListView):
    model = PersonProfile
    # template_name='person_changelist.html'
    context_object_name = 'people'

def personprofile(request):
    try:
        instance = PersonProfile.objects.get(user=request.user)
    except PersonProfile.DoesNotExist:
        instance = None
    if request.method == 'POST':
        form = PersonProfileForm(request.POST, instance=instance)
        if form.is_valid():
            if PersonProfile.objects.filter(user=request.user):
                obj = PersonProfile.objects.get(user=request.user)
                obj.user = request.user
                obj.country = form.cleaned_data['country']
                obj.save()
                city = form.cleaned_data['city']
                for c in city:
                    obj.city.add(c)
                    obj.save()
            else:
                user = request.user
                country = form.cleaned_data['country']
                city = form.cleaned_data['city']
                
                useprofile = PersonProfile(user=user, country=country)
                useprofile.save()
                for c in city:
                    useprofile.city.add(c)
                    useprofile.save()
            messages.success(request, 'Successfully updated.')
            return redirect('home')
    else:
        form = PersonProfileForm(instance=instance)
    userp = PersonProfile.objects.filter(user=request.user)
    context = {
            'form': form,
            'user': request.user,
            'userp': userp
    }
     # redirect to a new URL:
    return render(request, 'classapp/personprofile_form.html', context)

class PersonCreateView(CreateView):
    model = PersonProfile
    fields = ['country','city']
    success_url = reverse_lazy('person_changelist')

    def form_valid(self, form):
        user = self.request.user.id
        form.instance.user = user
        return super(PersonCreateView, self).form_valid(form)

class PersonUpdateView(UpdateView):
    model = PersonProfile
    form_class = PersonProfileForm
    success_url = reverse_lazy('person_changelist')


def load_cities(request):
    country_id = request.GET.get('country')
    cities = Places.objects.filter(district_id=country_id).order_by('name')
    return render(request, 'hr/city_dropdown_list_options.html', {'cities': cities})
