from django.db.models import Q
#basic import
from django.shortcuts import render, HttpResponse,redirect,HttpResponseRedirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.views.generic import View
import time
#Userlogin signup, import
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash,get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeForm, PasswordResetCompleteView, \
    PasswordResetConfirmView, PasswordResetView,PasswordResetForm,PasswordResetDoneView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
#LocAL IMPORT
from posts.models import TuitionPost
from tolet.models import Post
from .models import UserProfile, Contact, SSC,HigherStudies,HSC,AfterHsc,District,Subject,SubDistrict,Classes,TuitionClass
from .forms import (UserProfileForm, UserUpdateForm, ContactForm, \
    SSCForm,HSCForm,AfterHscForm,HigherStudiesForm,TuitionClassForm,SubjectForm,TuitionClassUpdateForm,SignUpForm)
#TOKEN  generator import
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
UserModel = get_user_model()

def handleSignup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # print(form.errors.as_data())
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('person/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(
                request, 'Please confirm From your email address to complete the registration and Then you can login')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'person/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.info(
            request, f"Thank you for your email confirmation.  Now you can login your account. {user}")
        return redirect('login')
    else:
        messages.warning(request, 'Activation link is invalid!')
        return redirect('signup')

def updateprofile(request):
    try:
        instance = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        instance = None
    username = request.user.username
    userp = User.objects.get(username=username)
    if request.method == 'POST':
        if instance:
            p_form = UserProfileForm(request.POST, request.FILES, instance=instance)
        else:
            p_form = UserProfileForm(request.POST, request.FILES)
        u_form= UserUpdateForm(request.POST , instance=request.user)
        if u_form.is_valid() and p_form.is_valid():
            profile_obj = p_form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            email =u_form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists() and userp.email != email:
                messages.warning(
                    request, 'Your Provided email is already in Use in another profile.')
                return redirect('updateprofile')
            elif userp.email == email:
                u_form.save()
            else:
                user = u_form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('person/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                email1 = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email1.send()
                messages.warning(request, ' Email Changed. Temporarily Your accound has been deactivated.')
                messages.info(request, 'Activate your account From your email address and only then you can login.')
                logout(request)
                return redirect('home')
            messages.success(request, 'Successfully updated.')
            return redirect('userprofile')
    else:
        u_form= UserUpdateForm( instance=request.user)
        p_form = UserProfileForm( instance=instance) 
    userp=UserProfile.objects.filter(user=request.user)
    context = {
            'u_form':u_form,
            'p_form':p_form,
            'user': request.user,
            'userp':userp
             }
        # redirect to a new URL:
    return render(request, 'person/updateprofile.html', context)

def handleLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="person/login.html",
                  context={"form": form})

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('home')
def changepass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password Has changed successfully!')
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'person/changepass.html', {'form': form})

class ResetPassword(PasswordResetView):
    template_name = 'person/reset_pass.html'

class ResetPasswordDone(PasswordResetDoneView):
    template_name = 'person/reset_pass_done.html'

class ResetPasswordConfirm(PasswordResetConfirmView):
    template_name = 'person/reset_pass_confirm.html'

class ResetPasswordComplete(PasswordResetCompleteView):
    template_name = 'person/reset_pass_complete.html'

def userlist(request):
    users=User.objects.all()
    district = District.objects.all()
    subject = Subject.objects.all()
    classes = Classes.objects.all()
    
    context = {
        'district': district,
        'subject': subject,
        'classes': classes,
        'users':users,
    }
    return render(request, 'person/person_list.html', context)


def teacherlist(request):
    if request.method == "POST":
        district=request.POST['district_i']
        subject=request.POST['subject_i']
        classes = request.POST['class_i']
        # print(district, subject, classes)
        if district or subject or classes:
            queryset = (Q(district__name__icontains=district)) & (
                Q(level__name__icontains=classes)) & (Q(subject__name__icontains=subject))
            results = TuitionClass.objects.filter(queryset).distinct()
        else:
            results = []
    return render(request, "person/teacher_list.html", {'results': results})

def notification(request):
    user = User.objects.get(username=request.user.username)
    qs = user.notifications.read()
    us = user.notifications.unread()
    return render(request, 'person/notification.html', {'qs': qs, 'us':us})
    
def markasread(request):
    user = User.objects.get(username=request.user.username)
    qs = user.notifications.unread()
    qs.mark_all_as_read()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class homeView(View):
    template_name= "person/home.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def userprofile(request):
    userp=UserProfile.objects.filter(user=request.user)
    query=request.user
    try:
        mypostauthor=TuitionPost.objects.filter(author=query)
    except TuitionPost.DoesNotExist:
        mypostauthor=None
    try:
        toletuser=Post.objects.filter(user=query)
    except Post.DoesNotExist:
        toletuser=None
    # myposts=myposts.union(mytolet)
    
    return render(request, 'person/userprofile.html',{'userp':userp, 'post':mypostauthor,'mytolet':toletuser})
   
def contact(request): 
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form= ContactForm(request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request, 'successfully Sent.')
            return redirect('userprofile')
    else:
        form = ContactForm() 
        
    context = {
            'form':form,
            'user': request.user 
            }
        # redirect to a new URL:
    return render(request, 'person/contact_us.html',context )


def updatessc(request):
    try:
        instance = SSC.objects.get(user=request.user)
    except SSC.DoesNotExist:
        instance = None
    if request.method == 'POST':
        if instance:
            form = SSCForm(request.POST, instance=instance)
        else:
            form = SSCForm(request.POST)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            messages.success(request, 'Successfully updated.')
            return redirect('userprofile')
    else:
        form = SSCForm(instance=instance)
    
    context = {
        'form': form,
    }
    # redirect to a new URL:
    return render(request, 'person/updatessc.html', context)


def updatehsc(request):
    try:
        instance = HSC.objects.get(user=request.user)
    except HSC.DoesNotExist:
        instance = None
    if request.method == 'POST':
        if instance:
            form = HSCForm(request.POST, instance=instance)
        else:
            form = HSCForm(request.POST)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            messages.success(request, 'Successfully updated.')
            return redirect('userprofile')
    else:
        form = HSCForm(instance=instance)

    context = {
        'form': form,
    }
    return render(request, 'person/updatehsc.html', context)


def afterhsc(request):
    try:
        instance = AfterHsc.objects.get(user=request.user)
    except AfterHsc.DoesNotExist:
        instance = None
    if request.method == 'POST':
        if instance:
            form = AfterHscForm(request.POST, instance=instance)
        else:
            form = AfterHscForm(request.POST)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            messages.success(request, 'Successfully updated.')
            return redirect('userprofile')
    else:
        form = AfterHscForm(instance=instance)

    context = {
        'form': form,
    }
    return render(request, 'person/updateafterhsc.html', context)


def postgraduate(request):
    try:
        instance = HigherStudies.objects.get(user=request.user)
    except HigherStudies.DoesNotExist:
        instance = None
    if request.method == 'POST':
        if instance:
            form = HigherStudiesForm(request.POST, instance=instance)
        else:
            form = HigherStudiesForm(request.POST)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            messages.success(request, 'Successfully updated.')
            return redirect('userprofile')
    else:
        form = HigherStudiesForm(instance=instance)

    context = {
        'form': form,
    }
    return render(request, 'person/updatepostgraduate.html', context)


def tuitionprofile(request):
    try:
        instance = TuitionClass.objects.get(user=request.user)
        obj = TuitionClass.objects.get(user=request.user)
    except TuitionClass.DoesNotExist:
        instance = None

    if request.method == 'POST':
        if instance:
            form = TuitionClassForm(request.POST, instance=instance)
        else:
            form = TuitionClassForm(request.POST)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            if obj.district == form.cleaned_data['district']:
                pass
            else:
                profile_obj.preferedPlace.set([])
                profile_obj.save()
            level = form.cleaned_data['level']
            profile_obj.level.set([])
            for l in level:
                profile_obj.level.add(l)
                profile_obj.save()
            subject = form.cleaned_data['subject']
            profile_obj.subject.set([])
            for f in subject:
                profile_obj.subject.add(f)
                profile_obj.save()
            profile_obj.save()
            messages.success(request, 'Successfully updated.')
            messages.warning(request, 'Now Add your Prefered Tuition Place of That District.')
            return redirect('tuitionprofileupdate')
    else:
        form = TuitionClassForm(instance=instance)

    context = {
        'form': form,
    }
    return render(request, 'person/tuitionprofile.html', context)


def tuitionprofileupdate(request):
    try:
        instance = TuitionClass.objects.get(user=request.user)
    except TuitionClass.DoesNotExist:
        instance = None
    if request.method == 'POST':
        if instance:
            form = TuitionClassUpdateForm(request.POST, instance=instance)
        else:
            form = TuitionClassUpdateForm(request.POST) 
        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            level = form.cleaned_data['level']
            for l in level:
                profile_obj.level.add(l)
                profile_obj.save()
            subject = form.cleaned_data['subject']
            for f in subject:
                profile_obj.subject.add(f)
                profile_obj.save()
            preferedPlace = form.cleaned_data['preferedPlace']
            for p in preferedPlace:
                profile_obj.preferedPlace.add(p)
                profile_obj.save()
            profile_obj.save()
            profile_obj.save()
            messages.success(request, 'Successfully updated.')
            return redirect('userprofile')
    else:
        form = TuitionClassUpdateForm(instance=instance)

    context = {
        'form': form,
    }
    return render(request, 'person/tuitionprofileupdate.html', context)
def otherprofile(request, slug):
    user = User.objects.get(username=slug)
    try:
        uSsc = user.ssc
    except:
        uSsc=None
    try:
        uHsc = user.hsc
    except:
        uHsc=None
    try:
        afterhsc = user.afterhsc
    except:
        afterhsc = None
    try:
        higherstudies = user.higherstudies
    except:
        higherstudies = None
    try:
        userp = user.userprofile
    except:
        userp = None
    try:
        tuitionprofile = user.tuitionclass
    except:
        tuitionprofile = None
    try:
        subject = tuitionprofile.subject.all()
    except:
        subject = None
    try:
        places = tuitionprofile.preferedPlace.all()
    except:
        places = None
    try:
        class_in = tuitionprofile.level.all()
    except:
        class_in = None
    context = {
        'user': user,
        'uSsc': uSsc,
        'uHsc': uHsc,
        'afterhsc': afterhsc,
        'higherstudies': higherstudies,
        'tuitionprofile': tuitionprofile,
        'subject': subject,
        'places': places,
        'class_in': class_in,
        'userp':userp
    }
    return render(request, 'person/otherprofile.html', context)
    

def load_cities(request):
    district_id = request.GET.get('district')
    cities = SubDistrict.objects.filter(district_id=district_id).order_by('name')
    return render(request, 'hr/city_dropdown_list_options.html', {'cities': cities})

def addsubject(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subcheck = Subject.objects.filter(name__icontains=name)
            if subcheck:
                messages.warning(
                    request, 'This subject allready includes in list.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                form.save()
                messages.success(request, 'Successfully Added this Subject.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = SubjectForm()
    return render(request, 'posts/addsubject.html', {'form': form, 'subjects': subjects})
