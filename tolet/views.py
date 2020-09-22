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
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def viewtolet(request):
    post= Post.objects.all()
    params = {
        'district': District.objects.all(),
        'category': Category.objects.all(),
        'area': Area.objects.all(),
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

# def imgup(request,id):
#     instance=Post.objects.get(id=id)
#     if request.method =='POST':
#         form = PostModelForm(instance=instance)
#         file_form = FileModelForm(request.POST, request.FILES)
#         files = request.FILES.getlist('file') #field name in model
#         if file_form.is_valid():
#             for f in files:
#                 file_instance = PostFile(file=f, feed=instance)
#                 file_instance.save()
#             messages.success(request, 'Successfully Added your post with image')
#             return redirect(f"/tolet/toletpost/{instance.id}")
#     else:
#         file_form = FileModelForm()
#         form = PostModelForm(instance=instance)
#     context={
#         'instance': instance,
#         'id': instance.id,
#         'file_form': file_form,
#         'form': form,
#     }
#     return render(request, 'tolet/imgup.html',context)
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

def toletcomment(request):
    if request.method=="POST":
        comment= request.POST.get("comment")
        user = request.user 
        postsno=request.POST.get("postsno")
        post =  Post.objects.get(id=postsno) 
        parentsno =  request.POST.get("parentsno") 
        image=user.userprofile.image 
        print(image)
        if parentsno == "":
            print("if")
            comments= ToletComment(comment=comment, user= user, post= post,image=image)
            comments.save()
            messages.success(request, 'Success! your comment have been posted successfully.')
        else:
            print("else")
            parent=ToletComment.objects.get(sno=parentsno)
            comments= ToletComment(comment=comment, user= user, post= post, parent=parent,image=image)
            comments.save()
            messages.success(request, 'Success! your reply have been posted successfully.')
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
        form = PostModelForm(instance=instance)
       
    context = {
            'form':form,
            'instance':instance
            }
        # redirect to a new URL:
    return render(request, 'tolet/updatetolet.html',context )
