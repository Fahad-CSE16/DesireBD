from django.contrib import admin
from django.urls import path, include
from . import views
from .views import homeView, ResetPassword,ResetPasswordComplete,ResetPasswordConfirm,ResetPasswordDone


urlpatterns = [
    path('', homeView.as_view(), name='home'),
    path('signup/', views.handleSignup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.handleLogin, name='login'),
    path('logout/', views.handleLogout, name='logout'),

    path('changepass/', views.changepass, name='changepass'),
    path('reset/password/',ResetPassword.as_view(), name='password_reset'),
    path('reset/password/done/', ResetPasswordDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',ResetPasswordConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', ResetPasswordComplete.as_view(), name='password_reset_complete'),


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
    path('userlist/', views.userlist, name='userlist'),
    path('teacherlist/', views.teacherlist, name='teacherlist'),
    


    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]
