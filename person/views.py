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
                request, 'Please confirm your email address to complete the registration')
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


class homeView(View):
    template_name= "person/home.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

def updateprofile(request):
    try:
        instance = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        instance = None
    username = request.user.username
    userp = User.objects.get(username=username)
    if request.method == 'POST':
        
        # create a form instance and populate it with data from the request:
        u_form= UserUpdateForm(request.POST , instance=request.user)
        p_form = UserProfileForm(request.POST ,request.FILES, instance=instance) 
        if u_form.is_valid() and p_form.is_valid():
            email =u_form.cleaned_data.get('email')
            
            if User.objects.filter(email=email).exists() and userp.email != email:
                messages.warning(request,'Your Provided email is already in Use in another profile.')
                return redirect('updateprofile')
            else:
                u_form.save()
            if UserProfile.objects.filter(user=request.user):
                obj=UserProfile.objects.get(user=request.user)
                obj.user= request.user
                obj.birth_date= p_form.cleaned_data['birth_date']
                obj.genre= p_form.cleaned_data['genre']
                obj.address= p_form.cleaned_data['address']
                obj.nationality = p_form.cleaned_data['nationality']
                obj.marital_status= p_form.cleaned_data['marital_status']
                obj.phone= p_form.cleaned_data['phone']
                obj.profession = p_form.cleaned_data['profession']
                obj.blood_group= p_form.cleaned_data['blood_group']
                obj.religion= p_form.cleaned_data['religion']
                obj.image= p_form.cleaned_data['image']
                obj.biodata = p_form.cleaned_data['biodata']
                obj.save()
                
            else:
                user= request.user
                birth_date= p_form.cleaned_data['birth_date']
                genre= p_form.cleaned_data['genre']
                address= p_form.cleaned_data['address']
                nationality= p_form.cleaned_data['nationality']
                marital_status= p_form.cleaned_data['marital_status']
                phone= p_form.cleaned_data['phone']
                profession = p_form.cleaned_data['profession']
                religion = p_form.cleaned_data['religion']
                blood_group = p_form.cleaned_data['blood_group']
                image= p_form.cleaned_data['image']
                biodata = p_form.cleaned_data['biodata']
                print("fahad")
                useprofile = UserProfile(user=user, birth_date=birth_date, biodata=biodata, genre=genre, address=address, nationality=nationality,
                                         marital_status=marital_status, phone=phone, profession=profession, blood_group=blood_group, religion=religion, image=image)
                useprofile.save()
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
            messages.success(request, 'successfully Sent.')
            form.save()
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
        # create a form instance and populate it with data from the request:
        form = SSCForm(request.POST, instance=instance)
        if form.is_valid() :
            if SSC.objects.filter(user=request.user):
                obj = SSC.objects.get(user=request.user)
                obj.user = request.user
                obj.group = form.cleaned_data['group']
                obj.institute = form.cleaned_data['institute']
                obj.gpa = form.cleaned_data['gpa']
                obj.board = form.cleaned_data['board']
                obj.passing_year = form.cleaned_data['passing_year']
                obj.save()
            else:
                user = request.user
                group = form.cleaned_data['group']
                institute = form.cleaned_data['institute']
                gpa = form.cleaned_data['gpa']
                board = form.cleaned_data['board']
                passing_year = form.cleaned_data['passing_year']
                useprofile = SSC(user=user, group=group, institute=institute, gpa=gpa, board=board, passing_year=passing_year)
                useprofile.save()
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
        # create a form instance and populate it with data from the request:
        form = HSCForm(request.POST, instance=instance)
        if form.is_valid():
            if HSC.objects.filter(user=request.user):
                obj = HSC.objects.get(user=request.user)
                obj.user = request.user
                obj.group = form.cleaned_data['group']
                obj.institute = form.cleaned_data['institute']
                obj.gpa = form.cleaned_data['gpa']
                obj.board = form.cleaned_data['board']
                obj.passing_year = form.cleaned_data['passing_year']
                obj.save()
            else:
                user = request.user
                group = form.cleaned_data['group']
                institute = form.cleaned_data['institute']
                gpa = form.cleaned_data['gpa']
                board = form.cleaned_data['board']
                passing_year = form.cleaned_data['passing_year']
                useprofile = HSC(user=user, group=group, institute=institute,
                                 gpa=gpa, board=board, passing_year=passing_year)
                useprofile.save()
            messages.success(request, 'Successfully updated.')
            return redirect('userprofile')
    else:
        form = HSCForm(instance=instance)

    context = {
        'form': form,
    }
    # redirect to a new URL:
    return render(request, 'person/updatehsc.html', context)


def afterhsc(request):
    try:
        instance = AfterHsc.objects.get(user=request.user)
    except AfterHsc.DoesNotExist:
        instance = None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AfterHscForm(request.POST, instance=instance)
        if form.is_valid():
            if AfterHsc.objects.filter(user=request.user):
                obj = AfterHsc.objects.get(user=request.user)
                obj.user = request.user
                obj.degree = form.cleaned_data['degree']
                obj.institute = form.cleaned_data['institute']
                obj.cgpa = form.cleaned_data['cgpa']
                obj.Etype = form.cleaned_data['Etype']
                obj.passing_year = form.cleaned_data['passing_year']
                obj.save()
            else:
                user = request.user
                degree = form.cleaned_data['degree']
                institute = form.cleaned_data['institute']
                cgpa = form.cleaned_data['cgpa']
                Etype = form.cleaned_data['Etype']
                passing_year = form.cleaned_data['passing_year']
                useprofile = AfterHsc(user=user, degree=degree, institute=institute,cgpa=cgpa, Etype=Etype, passing_year=passing_year)
                useprofile.save()
            messages.success(request, 'Successfully updated.')
            return redirect('userprofile')
    else:
        form = AfterHscForm(instance=instance)

    context = {
        'form': form,
    }
    # redirect to a new URL:
    return render(request, 'person/updateafterhsc.html', context)


def postgraduate(request):
    try:
        instance = HigherStudies.objects.get(user=request.user)
    except HigherStudies.DoesNotExist:
        instance = None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = HigherStudiesForm(request.POST, instance=instance)
        if form.is_valid():
            if HigherStudies.objects.filter(user=request.user):
                obj = HigherStudies.objects.get(user=request.user)
                obj.user = request.user
                obj.masters = form.cleaned_data['masters']
                obj.phd = form.cleaned_data['phd']
                obj.save()
            else:
                user = request.user
                masters = form.cleaned_data['masters']
                phd = form.cleaned_data['phd']
                useprofile = HigherStudies(user=user, masters=masters, phd=phd)
                useprofile.save()
            messages.success(request, 'Successfully updated.')
            return redirect('userprofile')
    else:
        form = HigherStudiesForm(instance=instance)

    context = {
        'form': form,
    }
    # redirect to a new URL:
    return render(request, 'person/updatepostgraduate.html', context)


def tuitionprofile(request):
    try:
        instance = TuitionClass.objects.get(user=request.user)
    except TuitionClass.DoesNotExist:
        instance = None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TuitionClassForm(request.POST, instance=instance)
        if form.is_valid():
            if TuitionClass.objects.filter(user=request.user):
                obj = TuitionClass.objects.get(user=request.user)
                obj.user = request.user
                obj.style = form.cleaned_data['style']
                obj.place = form.cleaned_data['place']
                obj.approach = form.cleaned_data['approach']
                obj.medium = form.cleaned_data['medium']
                if obj.district == form.cleaned_data['district']:
                    pass
                else:
                    obj.preferedPlace.set([])
                obj.district = form.cleaned_data['district']
                obj.high_education = form.cleaned_data['high_education']
                obj.salary = form.cleaned_data['salary']
                obj.status = form.cleaned_data['status']
                obj.days = form.cleaned_data['days']
                
                obj.save()
                level = form.cleaned_data['level']
                for l in level:
                    obj.level.add(l)
                    obj.save()
                subject = form.cleaned_data['subject']
                for f in subject:
                    obj.subject.add(f)
                    obj.save()
                
                # preferedPlace = form.cleaned_data['preferedPlace']
                # for p in preferedPlace:
                #     obj.preferedPlace.add(p)
                #     obj.save()
            else:
                user = request.user
                style = form.cleaned_data['style']
                place = form.cleaned_data['place']
                approach = form.cleaned_data['approach']
                medium = form.cleaned_data['medium']
                district = form.cleaned_data['district']
                high_education = form.cleaned_data['high_education']
                salary = form.cleaned_data['salary']
                status = form.cleaned_data['status']
                days = form.cleaned_data['days']
                level = form.cleaned_data['level']
                subject = form.cleaned_data['subject']
                useprofile = TuitionClass(
                    user=user, style=style, place=place, approach=approach, medium=medium, district=district, high_education=high_education, salary=salary, status=status, days=days)
                useprofile.save()
                for l in level:
                    useprofile.level.add(l)
                    useprofile.save()
                for f in subject:
                    useprofile.subject.add(f)
                    useprofile.save()
                # preferedPlace = form.cleaned_data['preferedPlace']
                # for p in preferedPlace:
                #     useprofile.preferedPlace.add(p)
                #     useprofile.save()
            messages.success(request, 'Successfully updated.')
            messages.warning(request, 'Now Add your Prefered Tuition Place of That District.')
            return redirect('tuitionprofileupdate')
    else:
        form = TuitionClassForm(instance=instance)

    context = {
        'form': form,
    }
    # redirect to a new URL:
    return render(request, 'person/tuitionprofile.html', context)


def tuitionprofileupdate(request):
    try:
        instance = TuitionClass.objects.get(user=request.user)
    except TuitionClass.DoesNotExist:
        instance = None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TuitionClassUpdateForm(request.POST, instance=instance)
        if form.is_valid():
            if TuitionClass.objects.filter(user=request.user):
                obj = TuitionClass.objects.get(user=request.user)
                obj.user = request.user
                obj.style = form.cleaned_data['style']
                obj.place = form.cleaned_data['place']
                obj.approach = form.cleaned_data['approach']
                obj.medium = form.cleaned_data['medium']
                obj.high_education = form.cleaned_data['high_education']
                obj.salary = form.cleaned_data['salary']
                obj.status = form.cleaned_data['status']
                obj.days = form.cleaned_data['days']

                obj.save()
                level = form.cleaned_data['level']
                for l in level:
                    obj.level.add(l)
                    obj.save()
                subject = form.cleaned_data['subject']
                for f in subject:
                    obj.subject.add(f)
                    obj.save()
                preferedPlace = form.cleaned_data['preferedPlace']
                for p in preferedPlace:
                    obj.preferedPlace.add(p)
                    obj.save()
            else:
                user = request.user
                style = form.cleaned_data['style']
                place = form.cleaned_data['place']
                approach = form.cleaned_data['approach']
                medium = form.cleaned_data['medium']
                district = form.cleaned_data['district']
                high_education = form.cleaned_data['high_education']
                salary = form.cleaned_data['salary']
                status = form.cleaned_data['status']
                days = form.cleaned_data['days']
                level = form.cleaned_data['level']
                subject = form.cleaned_data['subject']
                useprofile = TuitionClass(
                    user=user, style=style, place=place, approach=approach, medium=medium, district=district, high_education=high_education, salary=salary, status=status, days=days)
                useprofile.save()
                for l in level:
                    useprofile.level.add(l)
                    useprofile.save()
                for f in subject:
                    useprofile.subject.add(f)
                    useprofile.save()
                preferedPlace = form.cleaned_data['preferedPlace']
                for p in preferedPlace:
                    useprofile.preferedPlace.add(p)
                    useprofile.save()
            messages.success(request, 'Successfully updated.')
            return redirect('userprofile')
    else:
        form = TuitionClassUpdateForm(instance=instance)

    context = {
        'form': form,
    }
    # redirect to a new URL:
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
