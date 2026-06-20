from django import forms
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin

from posts.models import Post
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


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio']
        labels = {
            'bio': 'Your biography'
        }
        help_texts = {
            'bio': 'Max. 200 characters'
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Insert your bio...'})
        }


def edit_profile(request):
    profile_form = ProfileEditForm(instance=request.user)

    pinned_posts = Post.objects.filter(author=request.user, is_pinned=True)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action in ['update_bio', 'save_all']:
            profile_form = ProfileEditForm(request.POST, instance=request.user)

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Your profile was successfully updated!")

                return redirect('users:profile', username=request.user.username)

    context = {
        'profile_form': profile_form,
        'pinned_posts': pinned_posts,
    }

    return render(request, 'users/edit_profile.html', context)


@login_required
def choose_pinned_post(request):
    unpinned_posts = Post.objects.filter(author=request.user, is_pinned=False).order_by('-created_at')

    context = {
        'posts': unpinned_posts
    }
    return render(request, 'users/choose_pinned_post.html', context)

