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

def home(request):
    teachers = TuitionClass.objects.all().order_by('district__name')
    template = "person/home.html"
    context = {
        'teachers': teachers,
        
    }
    return render(request, template, context)
class homeView(View):
    template_name= "person/home.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)



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
