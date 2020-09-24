from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.views import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.views.generic import View,TemplateView
import time

class homeView(View):
    template_name = "person/home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
class WorkView(TemplateView):
    template_name='hr/how_works.html'