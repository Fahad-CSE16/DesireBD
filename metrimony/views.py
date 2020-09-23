from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import (Country, Education, Expectaion, Address, Body, Family, Height, Hobby, Language, Occupation, Personal_Info, Profession, Religion, Sir_name, State, Weight,Age,Company
                     )
from .forms import *
from person.models import District
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
            return HttpResponseRedirect('/metrimony/expectation/')
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
            return HttpResponseRedirect('/metrimony/hobby/')
    else:
        height=Height.objects.all().order_by('name')
        form = BodyForm(instance=instance,data_list=height)
    context = {
        'form': form
    }
    return render(request, 'metrimony/body.html', context)
def personal(request):
    try:
        instance = Personal_Info.objects.get(user=request.user)
    except Personal_Info.DoesNotExist:
        instance = None
    if request.method == 'POST':
        if instance:
            form = PersonalForm(request.POST,request.FILES, instance=instance)
        else:
            form = PersonalForm(request.POST, request.FILES)
        if form.is_valid():
            language = form.cleaned_data['mother_tongue']
            lancheck = Language.objects.filter(name=language)
            if not lancheck:
                Language.objects.create(name=language)

            sir_name = form.cleaned_data['sir_name']
            sircheck = Sir_name.objects.filter(name=sir_name)
            if not sircheck:
                Sir_name.objects.create(name=sir_name)
            religion = form.cleaned_data['religion']
            relcheck = Religion.objects.filter(name=religion)
            if not relcheck:
                Religion.objects.create(name=religion)
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            languages = form.cleaned_data['languages']
            for l in languages:
                profile_obj.languages.add(l)
                profile_obj.save()
            messages.success(request, 'Successfully updated.')
            return HttpResponseRedirect('/metrimony/address/')
    else:
        height=Sir_name.objects.all().order_by('name')
        language = Language.objects.all().order_by('name')
        religion=Religion.objects.all().order_by('name')
        form = PersonalForm(instance=instance,data_list=height,l_list=language,r_list=religion)
    context = {
        'form': form
    }
    return render(request, 'metrimony/personal_info.html', context)

def address(request):
    try:
        instance = Address.objects.get(user=request.user)
    except Address.DoesNotExist:
        instance = None
    if request.method == 'POST':
        if instance:
            form = AddressForm(request.POST,request.FILES, instance=instance)
        else:
            form = AddressForm(request.POST, request.FILES)
        if form.is_valid():
            district = form.cleaned_data['district']
            lancheck = District.objects.filter(name=district)
            if not lancheck:
                District.objects.create(name=district)

            district = form.cleaned_data['state']
            lancheck = State.objects.filter(name=district)
            if not lancheck:
                State.objects.create(name=district)

            sir_name = form.cleaned_data['birth_country']
            sircheck = Country.objects.filter(name=sir_name)
            if not sircheck:
                Country.objects.create(name=sir_name)

            sir_name = form.cleaned_data['residency_country']
            sircheck = Country.objects.filter(name=sir_name)
            if not sircheck:
                Country.objects.create(name=sir_name)

            sir_name = form.cleaned_data['grow_up_country']
            sircheck = Country.objects.filter(name=sir_name)
            if not sircheck:
                Country.objects.create(name=sir_name)
            
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            messages.success(request, 'Successfully updated.')
            return HttpResponseRedirect('/metrimony/family/')
    else:
        district=District.objects.all().order_by('name')
        country = Country.objects.all().order_by('name')
        state = State.objects.all().order_by('name')
        form = AddressForm(instance=instance,data_list=district, c_list=country, s_list=state)
    context = {
        'form': form
    }
    return render(request, 'metrimony/address.html', context)
def family(request):
    try:
        instance = Family.objects.get(user=request.user)
    except Family.DoesNotExist:
        instance = None
    if request.method == 'POST':
        if instance:
            form = FamilyForm(request.POST,request.FILES, instance=instance)
        else:
            form = FamilyForm(request.POST, request.FILES)
        if form.is_valid():

            sir_name = form.cleaned_data['fathers_occupation']
            sircheck = Profession.objects.filter(name=sir_name)
            if not sircheck:
                Profession.objects.create(name=sir_name)

            sir_name = form.cleaned_data['mothers_occupation']
            sircheck = Profession.objects.filter(name=sir_name)
            if not sircheck:
                Profession.objects.create(name=sir_name)
            
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            messages.success(request, 'Successfully updated.')
            return HttpResponseRedirect('/metrimony/occupation/')
    else:
        proffession = Profession.objects.all().order_by('name')
        form = FamilyForm(instance=instance,data_list=proffession)
    context = {
        'form': form
    }
    return render(request, 'metrimony/family.html', context)
def occupation(request):
    try:
        instance = Occupation.objects.get(user=request.user)
    except Occupation.DoesNotExist:
        instance = None
    if request.method == 'POST':
        if instance:
            form = OccupationForm(request.POST,request.FILES, instance=instance)
        else:
            form = OccupationForm(request.POST, request.FILES)
        if form.is_valid():

            sir_name = form.cleaned_data['occupation']
            sircheck = Profession.objects.filter(name=sir_name)
            if not sircheck:
                Profession.objects.create(name=sir_name)

            sir_name = form.cleaned_data['company']
            sircheck = Company.objects.filter(name=sir_name)
            if not sircheck:
                Company.objects.create(name=sir_name)
            
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            messages.success(request, 'Successfully updated.')
            return HttpResponseRedirect('/metrimony/body/')
    else:
        proffession = Profession.objects.all().order_by('name')
        company=Company.objects.all().order_by('name')
        form = OccupationForm(instance=instance, data_list=proffession,c_list=company)
    context = {
        'form': form
    }
    return render(request, 'metrimony/occupation.html', context)


def partnerchoose(u, expectation,user):
    try:
        use = user.personal_info
    except:
        use=None
    count = 0
    try:
        body = u.body
    except:
        body = None
    if body:
        if body.height >= expectation.min_height and body.height <= expectation.max_height:
            count = count + 1
        if body.complexion == expectation.complexion:
            count = count + 1
    try:
        address = u.address
    except:
        address = None
    if address:
        if address.residency_country == expectation.residency_country:
            count = count + 1
    try:
        occupation = u.occupation
    except:
        occupation = None
    if occupation:
        if occupation.occupation == expectation.profession:
            count = count + 1
    try:
        personal= u.personal_info
    except:
        personal = None
    if personal and use:
        if personal.marital_status == expectation.marital_status:
            count = count + 1
        if personal.age >= expectation.min_age and personal.age <= expectation.max_age:
            count = count + 1
        if personal.have_child == expectation.with_childern:
            count = count + 1
        if personal.religion == expectation.religion:
            count = count + 1
        if personal.gender != use.gender:
            count = count + 1
        if personal.diet == expectation.diet:
            count = count + 1
        if personal.do_u_smoke == expectation.smoking_havits:
            count = count + 1
        if personal.do_u_drink == expectation.drinking_havits:
            count = count + 1
        if personal.highest_degree_of_education == expectation.education:
            count = count + 1
    if count >= 9:
        return True
def partner(request):
    user = request.user
    users = User.objects.all().exclude(username=user.username)
    try:
        expect = user.ecpectation
    except:
        expect = None
    if expect:
        n=User.objects.filter(username=user.username)
        for u in users:
            if partnerchoose(u, expect, user):
                m=User.objects.filter(username=u.username)
                n = n.union(m)
        context = {
            'userss': n,
        }
        return render(request, 'metrimony/partners.html', context)
    else:
        return HttpResponseRedirect('/metrimony/personal/')



@login_required
def metrimony_profile(request, slug):
    user = User.objects.get(username=slug)
    context = {
        'user': user,
    }
    return render(request, 'metrimony/metrimony_profile.html', context)
