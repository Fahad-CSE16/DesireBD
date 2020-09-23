from django.contrib import admin
from django.urls import path, include


from .views import *
app_name = 'metrimony'
urlpatterns = [

    path('expectation/',expectaion, name='expectation'),
    path('hobby/', hobby, name='hobby'),
    path('body/', body, name='body'),
    path('personal/', personal, name='personal'),
    path('address/', address, name='address'),
    path('family/', family, name='family'),
    path('occupation/', occupation, name='occupation'),
    path('partners/', partner, name='partners'),
    path('metrimony_profile/<str:slug>/',  metrimony_profile, name='metrimony_profile'),


]
