from django.contrib import admin
from django.urls import path, include
from . import views
from .views import homeView


urlpatterns = [
    path('', homeView.as_view(), name='home'),
    path('signup/', views.handleSignup, name='handleSignup'),
    path('login/', views.handleLogin, name='handleLogin'),
    path('logout/', views.handleLogout, name='handleLogout'),
    path('changepass/', views.changepass, name='changepass'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    path('otherprofile/<str:slug>/', views.otherprofile, name='otherprofile'),
    path('updatessc/', views.updatessc, name='updatessc'),
    path('updatehsc/', views.updatehsc, name='updatehsc'),
    path('afterhsc/', views.afterhsc, name='afterhsc'),
    path('postgraduate/', views.postgraduate, name='postgraduate'),
    path('tuitionprofile/', views.tuitionprofile, name='tuitionprofile'),
    path('tuitionprofileupdate/', views.tuitionprofileupdate,name='tuitionprofileupdate'),
    path('about_us/', homeView.as_view(template_name='person/about_us.html'), name='about_us'),
    path('contact/', views.contact, name='contact'),
    path('addsubject/', views.addsubject, name='addsubject'),
    path('notification/', views.notification, name='notification'),
    path('markasread/', views.markasread, name='markasread'),
    


    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]
