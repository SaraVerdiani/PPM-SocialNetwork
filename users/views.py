from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin

from users.models import User, Follow


class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

class SignUpView(SuccessMessageMixin, CreateView):
    form_class = UserCreation
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')
    success_message = "Registration successful. Please log in."

class MyLoginView(LoginView):
    template_name = 'users/login.html'


def logout_view(request):
    if request.method == 'POST':
        logout(request)

        messages.success(request, "Logged out successfully")

        return redirect('users:login')

    return redirect('feed:home')

@login_required
def follow(request, username):
    target_user = get_object_or_404(User, username=username)

    if request.user == target_user:
        return redirect('profile', username=username)

    follow_record = Follow.objects.filter(follower=request.user, following=target_user)

    if follow_record.exists():
        follow_record.delete()
    else:
        Follow.objects.create(follower=request.user, following=target_user)

    next_page = request.META.get('HTTP_REFERER')

    if next_page:
        return redirect(next_page)

    return redirect('users:profile', username=username)
