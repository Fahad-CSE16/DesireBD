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
from .forms import TuitionPostForm,TuitionPostUpdateForm
from person.models import UserProfile
from posts.templatetags import extras
from notifications.signals import notify
# Create your views here.


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
        notify.send(user, recipient=receiver,
                verb=' has liked your post')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class postsView(View):
    template_name = "posts/home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def createpost(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TuitionPostForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            subject = form.cleaned_data['subject']
            for f in subject:
                obj.subject.add(f)
                obj.save()
            class_in = form.cleaned_data['class_in']
            for f in class_in:
                obj.class_in.add(f)
                obj.save()
            messages.success(request, 'Successfully Created Your Post.')
            messages.warning(
                request, 'Now Add your Prefered Tuition Place of your selected District.')
            return redirect(f"/posts/updatepost/{obj.sno}")
    else:
        form = TuitionPostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/createpost.html', context)


def updatepost(request, sno):
    try:
        instance = TuitionPost.objects.get(sno=sno)
    except TuitionPost.DoesNotExist:
        instance = None
    if request.method == 'POST':
        form = TuitionPostUpdateForm(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            preferedPlace = form.cleaned_data['preferedPlace']
            for f in preferedPlace:
                obj.preferedPlace.add(f)
                obj.save()
            messages.success(request, 'Successfully Updated with your Places')
            return redirect(f"/posts/{obj.sno}")
    else:
        form = TuitionPostUpdateForm(instance=instance)

    context = {
        'form': form,
        'instance': instance
    }
    return render(request, 'posts/updatepost.html', context)

def editpost(request, sno):
    # form = TuitionPostForm()
    # post = TuitionPost.objects.get(sno=sno)
    try:
        instance = TuitionPost.objects.get(sno=sno)
    except TuitionPost.DoesNotExist:
        instance = None
    if request.method == 'POST':
        form = TuitionPostForm(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            subject = form.cleaned_data['subject']
            for f in subject:
                obj.subject.add(f)
                obj.save()
            class_in = form.cleaned_data['class_in']
            for f in class_in:
                obj.class_in.add(f)
                obj.save()
            messages.success(request, 'Successfully Edited Your Post')
            messages.warning(request, 'Now select some places of your selected district')
            return redirect(f"/posts/updatepost/{obj.sno}")
    else:
        form = TuitionPostForm(instance=instance)

    context = {
        'form': form,
        'instance': instance
    }
    return render(request, 'posts/editpost.html', context)


def viewpost(request):
    posts = TuitionPost.objects.all()
    
    params = {'posts': posts}
    return render(request, 'posts/viewpost.html', params)


def search(request):
    if request.method == 'POST':
        query = request.POST.get('search').lower()

        try:
            mypoststitle = TuitionPost.objects.filter(preferedPlace__icontains=query)
            mypostscontent = TuitionPost.objects.filter(content__icontains=query)
            myposts = mypoststitle.union(mypostscontent)

        except TuitionPost.DoesNotExist:
            myposts = None
        try:
            tolettitle = Post.objects.filter(text__icontains=query)
            tolettitle1 = Post.objects.filter(village__icontains=query)
            tolettitle2 = Post.objects.filter(upozila__icontains=query)
            tolettitle3 = Post.objects.filter(division__icontains=query)
            tolettitle4 = Post.objects.filter(area__icontains=query)
            mytolet = Post.objects.filter(Zilla__icontains=query)
            mytolet = mytolet.union(tolettitle)
            mytolet = mytolet.union(tolettitle1)
            mytolet = mytolet.union(tolettitle2)
            mytolet = mytolet.union(tolettitle3)
            mytolet = mytolet.union(tolettitle4)

        except Post.DoesNotExist:
            mytolet = None
        return render(request, "search.html", {'post': myposts, 'mytolet': mytolet})
    else:
        return render(request, "search.html", {})


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
    context = {
        'post': post,
        'comments': comments,
        'replyDict': replyDict,
        'userp': userp,
        'like': like,
        'liked': liked,
        'view':view
    }
    return render(request, 'posts/blogpost.html', context)


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        postsno = request.POST.get("postsno")
        post = TuitionPost.objects.get(sno=postsno)
        user = request.user
        receiver = User.objects.filter(username=post.author).first()
        parentsno = request.POST.get("parentsno")
        print(user)
        image = request.user.userprofile.image
        if parentsno == "":
            comments = BlogComment(
                comment=comment, user=user, tuitionpost=post, image=image)
            comments.save()
            if receiver != request.user:
                notify.send(user, recipient=receiver,verb=' has commented on your post')
            messages.success(request, 'Success! your comment have been posted successfully.')
        else:
            parent = BlogComment.objects.get(sno=parentsno)
            comments = BlogComment(
                image=image, comment=comment, user=user, tuitionpost=post, parent=parent)
            comments.save()
            receiver2 = parent.user
            if receiver != receiver2 and receiver != request.user:
                notify.send(user, recipient=receiver,
                        verb=' has replied  on someones comment in your post')
            if  receiver2  != request.user:
                notify.send(user, recipient=receiver2,
                        verb=' has replied to your comment')
            messages.success( request, 'Success! your reply have been posted successfully.')
    return redirect(f"/posts/{post.sno}")


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



