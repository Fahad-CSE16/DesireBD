from django.shortcuts import render
from .models import (Country, Education, Expectaion, Address, Body, Family, Height, Hobby, Language, Occupation, Personal_Info, Profession, Religion, Sir_name, State, Weight
                     )
from .forms import *
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
    if request.method == 'POST':
        if instance:
            form = ExpectaionForm(request.POST, instance=instance)
        else:
            form = ExpectaionForm(request.POST)
        if form.is_valid():

            education = form.cleaned_data['education']
            educheck = Education.objects.filter(name=education)
            if not educheck:
                Education.objects.create(name=education)

            religion = form.cleaned_data['religion']
            relcheck = Religion.objects.filter(name=religion)
            if not relcheck:
                Religion.objects.create(name=religion)

            profession = form.cleaned_data['profession']
            procheck = Profession.objects.filter(name=profession)
            if not procheck:
                Profession.objects.create(name=profession)

            height = form.cleaned_data['max_height']
            heicheck = Height.objects.filter(name=height)
            if not heicheck:
                Height.objects.create(name=height)

            height2 = form.cleaned_data['min_height']
            hei2check = Height.objects.filter(name=height2)
            if not hei2check:
                Height.objects.create(name=height2)

            weight = form.cleaned_data['max_age']
            weicheck = Weight.objects.filter(name=weight)
            if not weicheck:
                Weight.objects.create(name=weight)

            weight2 = form.cleaned_data['min_age']
            wei2check = Weight.objects.filter(name=weight2)
            if not wei2check:
                Weight.objects.create(name=weight2)

            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            messages.success(request, 'Successfully updated.')
            return redirect('userprofile')
    else:
        education = Education.objects.all().order_by('name')
        profession = Profession.objects.all().order_by('name')
        religion = Religion.objects.all().order_by('name')
        height=Height.objects.all().order_by('name')
        weight=Weight.objects.all().order_by('name')
        form = ExpectaionForm(instance=instance, data_list=education, a_list=profession, r_list=religion, h_list=height, w_list=weight)
    context = {
        'form': form
    }
    return render(request, 'metrimony/expectation.html', context)


def hobby(request):
    try:
        instance = Hobby.objects.get(user=request.user)
    except Hobby.DoesNotExist:
        instance = None
    if request.method == 'POST':
        if instance:
            form = HobbyForm(request.POST, instance=instance)
        else:
            form = HobbyForm(request.POST)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            messages.success(request, 'Successfully updated.')
            return redirect('userprofile')
    else:

        form = HobbyForm(instance=instance)
    context = {
        'form': form
    }
    return render(request, 'metrimony/hobby.html', context)
def body(request):
    try:
        instance = Body.objects.get(user=request.user)
    except Body.DoesNotExist:
        instance = None
    if request.method == 'POST':
        if instance:
            form = BodyForm(request.POST, instance=instance)
        else:
            form = BodyForm(request.POST)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            messages.success(request, 'Successfully updated.')
            return redirect('userprofile')
    else:
        height=Height.objects.all().order_by('name')
        form = BodyForm(instance=instance,data_list=height)
    context = {
        'form': form
    }
    return render(request, 'metrimony/body.html', context)
