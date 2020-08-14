from django.contrib import admin
from django.urls import path, include
from . import views

from .views import postsView
urlpatterns = [
    
    path('', postsView.as_view(), name='posts'),
    path('createpost/', views.createpost, name='createpost'),
    # path('viewsubjects/', views.viewsubjects, name='viewsubjects'),
    
    path('viewpost/', views.viewpost, name='viewpost'),
    path('postcomment/', views.postComment, name='postComment'),
    path('<int:sno>/', views.blogPost, name='blogPost'),
    path('deletepost/<int:sno>/', views.deletepost, name='deletepost'),
    path('likepost/<int:sno>/', views.likepost, name='likepost'),
    path('editpost/<int:sno>/', views.editpost, name='editpost'),
    path("search/", views.search, name="search"),
    path('deletecomment/', views.deletecomment, name='deletecomment'),

]
