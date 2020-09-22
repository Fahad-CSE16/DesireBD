from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('posttolet/', views.posttolet, name='posttolet'),
    path('likepost/<int:sno>/', views.likepost, name='likepost'),
    path('viewtolet/', views.viewtolet, name='viewtolet'),
    path('toletcomment/', views.toletcomment, name='toletcomment'),
    # path('imgup/<int:id>/', views.imgup, name='imgup'),
    path('deletetolet/<int:id>/', views.deletetolet, name='deletetolet'),
    path('deletephoto/<int:id>/', views.deletephoto, name='deletephoto'),
    path('deletecomment', views.deletecomment, name='deletecomment'),
    path('addphoto/<int:id>/', views.addphoto, name='addphoto'),
    path('edittolet/<int:id>/', views.edittolet, name='edittolet'),
    path('toletpost/<int:sno>/', views.toletpost, name='toletpost'),
]
