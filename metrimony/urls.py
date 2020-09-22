from django.contrib import admin
from django.urls import path, include


from .views import *
app_name = 'metrimony'
urlpatterns = [

    path('expectation/',expectaion, name='expectation'),
    path('hobby/', hobby, name='hobby'),
    path('body/', body, name='body'),

]
