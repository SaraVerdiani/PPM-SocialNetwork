from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.models import User


class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

class Authentication(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "email")

class SignUpView(CreateView):
    form_class = UserCreation
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')

class MyLoginView(LoginView):
    form_class = Authentication
    template_name = 'users/login.html'
