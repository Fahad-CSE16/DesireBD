from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.views.generic import View
import time
from math import ceil
from .models import TuitionPost, BlogComment
from tolet.models import Post, PostFile
from person.models import Subject, District, Classes
from .forms import TuitionPostForm, TuitionPostUpdateForm
from person.forms import ContactForm
from person.models import UserProfile, Contact
from posts.templatetags import extras
from notifications.signals import notify
# Create your views here.
from django.views import generic, View
from django.urls import reverse_lazy
from django.db.models import Q

def filterpost(request):
    if request.method == "POST":
        district = request.POST['district_i']
        subject = request.POST['subject_i']
        classes = request.POST['class_i']
        # print(district, subject, classes)
        if district or subject or classes:
            queryset = (Q(district__name__icontains=district)) & (
                Q(class_in__name__icontains=classes)) & (Q(subject__name__icontains=subject))
            results = TuitionPost.objects.filter(queryset).distinct()
        else:
            results = []
    return render(request, "posts/filterpost.html", {'results': results})

def likepost(request, sno):
    post = get_object_or_404(TuitionPost, sno=sno)
    user = request.user
    receiver = User.objects.filter(username=post.author).first()
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
        # notify.send(user, recipient=receiver,
        #             verb=' has unliked your post')
    else:
        post.likes.add(request.user)
        liked = True
        if user != receiver:
            notify.send(user, recipient=receiver,verb=" has liked your post" + f''' <a class =" btn btn-primary btn-sm " href="/posts/post/{post.sno}/">go</a> ''')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def authorcontact(request, sno):
    post=TuitionPost.objects.get(sno=sno)
    if request.method == 'POST':
        user = request.user
        receiver= User.objects.get(username=post.author)
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        if form.is_valid():
            email= form.cleaned_data['email']
            content = form.cleaned_data['content']
            phone=form.cleaned_data['phone']
            # form.save()
            notify.send(user, recipient=receiver,  verb="is applying for your tuition teacher, EMail: "+str(email)+" Phone: " + str(
                phone)+ f''' <a class =" btn btn-primary btn-sm " href="/profile/otherprofile/{user.username}/"> View</a> Teachers profile ''' )
            messages.success(request, 'successfully Sent.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = ContactForm()
    context = {
        'form': form,
        'user': request.user,
        'post':post
    }
    # redirect to a new URL:
    return render(request, 'posts/contact.html', context)

class postsView(View):
    template_name = "posts/home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

def receiverchoose(j, k):
    count=0
    if j.district == k.district:
        count = count + 1
    for i in j.medium:
        for l in k.medium:
            if i==l:
                count = count + 1
                break
    for i in j.subject.all():
        for l in k.subject.all():
            if i == l:
                count = count + 1
                break
    for i in j.level.all():
        for l in k.class_in.all():
            if i == l:
                count = count + 1
                break
    if count >= 3:
        return True
class CreatePostView(generic.CreateView):
    model = TuitionPost
    form_class = TuitionPostForm
    template_name = 'posts/createpost.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Successfully Created Your Post.')
        messages.warning(self.request, 'Now Add your Prefered Tuition Place of your selected District.')
        return super().form_valid(form)
    def get_success_url(self):
        id = self.object.sno
        user = self.request.user
        us = User.objects.all()
        for i in us:
            try:
                j = i.tuitionclass
            except:
                j = None
            if j:
                if receiverchoose(j, self.object):
                    receiver = i
                    if receiver != user:
                        notify.send(user, recipient=receiver, level='success',  verb="is searching for a teacher for "+str(self.object.medium)+" for " + str(
                            self.object.class_in.all().first())+" for subject " + str(self.object.subject.all().first()) + f''' <a class =" btn btn-primary btn-sm " href="/posts/post/{self.object.sno}">go</a> ''')
        
        return reverse_lazy('posts:update', kwargs={'pk': id})
class EditPostView(generic.UpdateView):
    model = TuitionPost
    form_class = TuitionPostForm
    template_name = 'posts/editpost.html'
    def get_success_url(self):
        id = self.kwargs['pk']
        return reverse_lazy('posts:update', kwargs={'pk': id})
class UpdatePostView(generic.UpdateView):
    model = TuitionPost
    form_class = TuitionPostUpdateForm
    template_name = 'posts/updatepost.html'
    def get_success_url(self):
        id = self.kwargs['pk']
        return reverse_lazy('posts:blogPost', kwargs={'sno': id})



def search(request):
    query = request.POST.get('q', '')
    print(query)
    print('f')
    if query:
        queryset = (Q(medium__icontains=query)) | (
            Q(content__icontains=query)) | (Q(subject__name__icontains=query)) | (Q(preferedPlace__name__icontains=query)) | (Q(class_in__name__icontains=query)) | (Q(district__name__icontains=query))
        results = TuitionPost.objects.filter(queryset).distinct()
    else:
       results = []
    if query:
        queryset = (Q(details__icontains=query)) | (Q(category__name__icontains=query)) | (Q(area__icontains=query)) | (Q(location__icontains=query)) | (Q(rent__icontains=query)) | (Q(district__name__icontains=query))
        mytolet = Post.objects.filter(queryset).distinct()
    else:
        mytolet = []
    return render(request, "search.html", {'results': results, 'mytolet': mytolet, 'query':query})

def blogPost(request, sno):
    post = TuitionPost.objects.filter(sno=sno).first()
    post.views.add(request.user)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    like = post.total_likes()
    view = post.total_views()
    comments = BlogComment.objects.filter(tuitionpost=post, parent=None)
    replies = BlogComment.objects.filter(tuitionpost=post).exclude(parent=None)
    replyDict = {}
    userp = UserProfile.objects.filter(user=request.user)
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    subject=post.subject.all()
    class_in=post.class_in.all()
    preferedPlace = post.preferedPlace.all()
    context = {
        'post': post,
        'comments': comments,
        'replyDict': replyDict,
        'userp': userp,
        'like': like,
        'liked': liked,
        'view': view,
        'subject': subject,
        'class_in': class_in,
        'preferedPlace':preferedPlace
    }
    return render(request, 'posts/blogpost.html', context)


def viewpost(request):
    posts = TuitionPost.objects.all().order_by('timeStamp')
    district = District.objects.all().order_by('name')
    subject = Subject.objects.all().order_by('name')
    classes = Classes.objects.all().order_by('name')
    params = {
        'posts': posts,
        'subject': subject,
        'classes': classes,
        'district': district

    }
    return render(request, 'posts/viewpost.html', params)

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        postsno = request.POST.get("postsno")
        post = TuitionPost.objects.get(sno=postsno)
        user = request.user
        receiver = User.objects.filter(username=post.author).first()
        parentsno = request.POST.get("parentsno")
        try:
            j = request.user.userprofile
        except:
            j = None
        if j:
            image = j.image
            if parentsno == "":
                comments = BlogComment(
                    comment=comment, user=user, tuitionpost=post, image=image)
                comments.save()
                if receiver != request.user:
                    notify.send(user, recipient=receiver,verb=" has commented on your post" +f''' <a class =" btn btn-primary btn-sm " href="/posts/post/{post.sno}">go</a> ''') 
                messages.success(request, 'Success! your comment have been posted successfully.')
            else:
                parent = BlogComment.objects.get(sno=parentsno)
                comments = BlogComment(
                    image=image, comment=comment, user=user, tuitionpost=post, parent=parent)
                comments.save()
                receiver2 = parent.user

                if receiver != receiver2 and receiver != request.user:
                    notify.send(user, recipient=receiver,
                            verb=" has replied  on someones comment in your post" +f''' <a class =" btn btn-primary btn-sm " href="/posts/post/{post.sno}">go</a> ''')
                if  receiver2  != request.user:
                    notify.send(user, recipient=receiver2,
                            verb=" has replied to your comment" +f''' <a class =" btn btn-primary btn-sm " href="/posts/post/{post.sno}">go</a> ''')
                messages.success(request, 'Success! your reply have been posted successfully.')
        else:
            messages.warning(request, 'Error! Please make a profile  first to comment')
            return redirect(f"/profile/updateprofile/")
    return redirect(f"/posts/post/{post.sno}")
    
def deletecomment(request):
    if request.method == "POST":
        parentsno = request.POST.get("parentsno")
        comment = BlogComment.objects.get(sno=parentsno)
        postsno = request.POST.get("postsno")
        post = TuitionPost.objects.get(sno=postsno)
        if request.user == comment.user:
            comment.delete()
        else:
            raise PermissionDenied
    messages.success(request, 'Successfully Deleted Your Comment')
    return redirect(f"/posts/{post.sno}")

def deletepost(request, sno):
    post = TuitionPost.objects.get(sno=sno)
    if request.user == post.author:
        post.delete()
    else:
        raise PermissionDenied
    messages.success(request, 'Successfully Deleted your Post.')
    return redirect('/posts/viewpost')
