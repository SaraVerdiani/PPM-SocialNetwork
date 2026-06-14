from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import CreateView

from users.models import User


class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

class SignUpView(CreateView):
    form_class = UserCreation
    template_name = 'users/signup.html'
