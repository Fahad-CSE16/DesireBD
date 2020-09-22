from django.contrib import admin
from django.urls import path, include


from .views import *
app_name = 'metrimony'
urlpatterns = [

    path('expectaion/',expectaion, name='expectation'),

]
