from django.db.models import Q
from django.shortcuts import render, HttpResponse,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
import time
from .models import PostFile, Post, ToletComment,Area, Category
from person.models import District

from .forms import PostModelForm, FileModelForm
# from .models import FeedFile
from person.models import UserProfile
from math import ceil
from django.core.exceptions import PermissionDenied
# Create your views here.

def likepost(request, sno):
    post = get_object_or_404(Post, id=sno)
    user = request.user
    receiver = User.objects.filter(username=post.user).first()
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        if user != receiver:
            notify.send(user, recipient=receiver,verb=" has liked your post" + f''' <a class =" btn btn-primary btn-sm " href="/tolet/toletpost/{post.id}/">go</a> ''')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def viewtolet(request):
    post = Post.objects.all().order_by('-timestamp')
    params = {
        'district': District.objects.all().order_by('name'),
        'category': Category.objects.all().order_by('name'),
        'area': Area.objects.all().order_by('name'),
        'post':post,
    }
    return render(request, 'tolet/viewtolet.html', params)

def posttolet(request):
    user = request.user
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        file_form = FileModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        if form.is_valid() and file_form.is_valid():
            area = form.cleaned_data['area']
            print(area)
            subcheck = Area.objects.filter(name=area)
            if not subcheck:
                Area.objects.create(name=area)
            feed_instance = form.save(commit=False)
            feed_instance.user = user
            feed_instance.save()
            for f in files:
                file_instance = PostFile(file=f, feed=feed_instance)
                file_instance.save()
            messages.success(request, 'Post Created Successfully. ')
            return redirect(f"/tolet/toletpost/{feed_instance.id}")
        
    else:
        area_list=Area.objects.all().order_by('name')
        file_form = FileModelForm()
        form = PostModelForm(data_list=area_list)
    context={
        'form': form,
        'file_form': file_form,
    }
    return render(request, 'tolet/posttolet.html',context)

def addphoto(request,id):
    instance=Post.objects.get(id=id)
    if request.method == 'POST':
        file_form = FileModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('file') #field name in model
        if file_form.is_valid():
            for f in files:
                file_instance = PostFile(file=f, feed=instance)
                file_instance.save()
        messages.success(request, 'Successfully Added your post with image')
        return redirect(f"/tolet/toletpost/{instance.id}")
    else:
        file_form = FileModelForm()
        form = PostModelForm(instance=instance)
    context={
        
        'id': instance.id,
        'file_form': file_form,
        'form': form,
    }
    return render(request, 'tolet/addphoto.html',context)
from notifications.signals import notify

def toletcomment(request):
    if request.method=="POST":
        comment= request.POST.get("comment")
        postsno=request.POST.get("postsno")
        parentsno =  request.POST.get("parentsno") 
        post = Post.objects.get(id=postsno)
        user = request.user
        receiver = User.objects.filter(username=post.user).first() 
        try:
            j = request.user.userprofile
        except:
            j = None
        if j:
            image = j.image
            if parentsno == "":
                comments = ToletComment(
                    comment=comment, user=user, post=post, image=image)
                comments.save()
                if receiver != request.user:
                    notify.send(user, recipient=receiver, verb=" has commented on your post" + f''' <a class =" btn btn-primary btn-sm " href="/tolet/toletpost/{post.id}">go</a> ''')
                    messages.success(request, 'Success! your comment have been posted successfully.')
            else:
                parent = ToletComment.objects.get(sno=parentsno)
                comments = ToletComment(
                    image=image, comment=comment, user=user, post=post, parent=parent)
                comments.save()
                receiver2 = parent.user

                if receiver != receiver2 and receiver != request.user:
                    notify.send(user, recipient=receiver,
                            verb=" has replied  on someones comment in your post" +f''' <a class =" btn btn-primary btn-sm " href="/tolet/toletpost/{post.id}">go</a> ''')
                    messages.success(request, 'Success! your comment have been posted successfully.')
                if  receiver2  != request.user:
                    notify.send(user, recipient=receiver2,
                            verb=" has replied to your comment" +f''' <a class =" btn btn-primary btn-sm " href="/tolet/toletpost/{post.id}">go</a> ''')
                    messages.success(request, 'Success! your reply have been posted successfully.')
        else:
            messages.warning(request, 'Error! Please make a profile  first to comment')
            return redirect(f"/profile/updateprofile/")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def toletpost(request, sno):
    feed= Post.objects.filter(id=sno).first()
    feed.views.add(request.user)
    liked = False
    if feed.likes.filter(id=request.user.id).exists():
        liked = True
    like = feed.total_likes()
    view = feed.total_views()

    try:
        p = feed.files.all()
    except feed.DoesNotExist:
        p = None 
    comments=ToletComment.objects.filter(post=feed, parent= None)
    replies=ToletComment.objects.filter(post=feed).exclude(parent=None)
    replyDict={}
    userp=UserProfile.objects.filter(user=request.user)
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    file_form=FileModelForm()
    context = {
        'like': like,
        'liked': liked,
        'view': view,
        'post': feed,
        'pic': p,
        'comments': comments,
        'replyDict': replyDict,
        'userp': userp,
        'file_form':file_form,
    }
    return render(request, 'tolet/toletpost.html', context)
def deletecomment(request): 
    if request.method=="POST":
        parentsno=request.POST.get("parentsno")
        comment =  ToletComment.objects.get(sno=parentsno)
        postsno=request.POST.get("postsno")
        post =  Post.objects.get(id=postsno) 
        if request.user == comment.user:
            comment.delete()
        else:
            raise PermissionDenied
    messages.success(request, 'Successfully Deleted Your Comment')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def deletetolet(request, id):
    feed= Post.objects.get(id=id)
    if request.user == feed.user:
        feed.delete()
    else:
        raise PermissionDenied
    messages.success(request, 'Successfully Deleted your Post.')
    return redirect('/tolet/viewtolet')
def deletephoto(request, id):
    feedfile= PostFile.objects.get(id=id)
    feedfile.delete()
    messages.success(request, 'Successfully Deleted your Photo')
    # now redirect to that same page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def edittolet(request, id): 
    form = PostModelForm()
    feed=Post.objects.get(id=id)
    try:
        instance = Post.objects.get(id=id)
    except Post.DoesNotExist:
        instance = None
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance= form
            instance.save()
            messages.success(request, 'Successfully Edited')
            return redirect(f"/tolet/toletpost/{feed.id}")
    else:
        area_list=Area.objects.all().order_by('name')
        
        form = PostModelForm(instance=instance,data_list=area_list)
       
    context = {
            'form':form,
            'instance':instance
            }
        # redirect to a new URL:
    return render(request, 'tolet/updatetolet.html',context )


def filterpost(request):
    if request.method == "POST":
        district = request.POST['district_i']
        category = request.POST['category_i']
        area = request.POST['area_i']
        # print(district, subject, classes)
        if district or category or area:
            queryset = (Q(district__name__icontains=district)) & (
                Q(area__icontains=area)) & (Q(category__name__icontains=category))
            results = Post.objects.filter(queryset).distinct().order_by('-timestamp')
        else:
            results = []
    return render(request, "tolet/filterpost.html", {'results': results})
