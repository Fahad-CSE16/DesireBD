from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser
from rest_framework import permissions, viewsets
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from person.models import *
from tolet.models import *
from posts.models import *
from .permissions import IsOwnerOrReadOnly, IsOwnerOrIsAdminOrReadOnly
from . serializers import *

# Create your views here.
class ApiRoot(APIView):
    def get(self, request, format=None):
        return Response({
            'users': reverse('users', request=request, format=format),
            'posts': reverse('posts', request=request, format=format),
            'comments': reverse('comments', request=request, format=format),
            'tuitionposts': reverse('tuitionposts', request=request, format=format),
            'blogcomments': reverse('blogcomments', request=request, format=format),
            'subjects': reverse('subjects', request=request, format=format),
            'classes': reverse('classes', request=request, format=format),
            'subdistricts': reverse('subdistricts', request=request, format=format),
            'notifications': reverse('notifications', request=request, format=format),
        })

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TuitionPostViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = TuitionPost.objects.all()
    serializer_class = TuitionPostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
class BlogCommentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer
    

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ToletComment.objects.all()
    serializer_class = ToletCommentSerializer
    
#sevaral used model viewsets starts from here
class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
class ClassesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer
class DistrictViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
class SubDistrictViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SubDistrict.objects.all()
    serializer_class = SubDistrictSerializer
