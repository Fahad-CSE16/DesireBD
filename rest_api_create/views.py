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
# from .permissions import IsOwnerOrReadOnly, IsOwnerOrIsAdminOrReadOnly
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
        })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TuitionPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TuitionPost.objects.all()
    serializer_class = TuitionPostSerializer    
class BlogCommentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer
    
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer   
class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ToletComment.objects.all()
    serializer_class = ToletCommentSerializer
    
#sevaral used model viewsets starts from here
class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
class ClassesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer
class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
class SubDistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubDistrict.objects.all()
    serializer_class = SubDistrictSerializer
