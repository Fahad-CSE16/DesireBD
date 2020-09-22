from django.shortcuts import render
from .models import (Country, Education, Expectaion, Address, Body, Family, Height, Hobby, Language, Occupation, Personal_Info, Profession, Religion, Sir_name, State, Weight
                     )
from .forms import ExpectaionForm
from django.db.models import Q
#basic import
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.views.generic import View

#Userlogin signup, import
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
#TOKEN  generator import
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
UserModel = get_user_model()

# Create your views here.


def expectaion(request):
    try:
        instance = Expectaion.objects.get(user=request.user)
    except Expectaion.DoesNotExist:
        instance = None
    print(instance)
    if request.method == 'POST':
        if instance:
            form = ExpectaionForm(request.POST, instance=instance)
        else:
            form = ExpectaionForm(request.POST)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            messages.success(request, 'Successfully updated.')
            return redirect('userprofile')
    else:
        eduacion=Education.objects.all()
        form = ExpectaionForm(instance=instance)
    context = {
        'form': form
    }
    return render(request, 'metrimony/expectation.html', context)
