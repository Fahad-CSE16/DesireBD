from django.contrib import admin
from django.urls import path, include
from . import views

from .views import *
app_name='posts'
urlpatterns = [
    
    path('', postsView.as_view(), name='posts'),
    path('createpost/', views.createpost, name='createpost'),
    path('updatepost/<int:pk>/', UpdatePostView.as_view(), name='update'),
    path('editpost/<int:pk>/',EditPostView.as_view(), name='editpost'),
    # path('viewsubjects/', views.viewsubjects, name='viewsubjects'),
    
    path('viewpost/', views.viewpost, name='viewpost'),
    path('filterpost/', views.filterpost, name='filterpost'),
    path('postcomment/', views.postComment, name='postComment'),
    path('post/<int:sno>/', views.blogPost, name='blogPost'),
    path('deletepost/<int:sno>/', views.deletepost, name='deletepost'),
    path('authorcontact/<int:sno>/', views.authorcontact, name='authorcontact'),
    path('likepost/<int:sno>/', views.likepost, name='likepost'),

    path("search/", views.search, name="search"),
    path('deletecomment/', views.deletecomment, name='deletecomment'),

]
