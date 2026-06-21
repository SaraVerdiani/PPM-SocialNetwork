from django import forms
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
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
        return redirect('users:profile', username=username)

    follow_record = Follow.objects.filter(follower=request.user, following=target_user).first()

    if follow_record:
        follow_record.delete()
    else:
        is_accepted = not target_user.is_private
        Follow.objects.create(follower=request.user, following=target_user, is_accepted=is_accepted)

    return redirect(request.META.get('HTTP_REFERER', '/'))


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio', 'is_private']
        labels = {
            'bio': 'Your biography',
            'is_private': 'Make profile private',
        }
        help_texts = {
            'bio': 'Max. 200 characters',
            'is_private': 'If enabled, only approved followers can see your posts.'
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


@login_required
def follow_requests(request):
    if not request.user.is_private:
        return redirect('feed:home')

    pending_requests = Follow.objects.filter(following=request.user, is_accepted=False).order_by('-id')

    context = {
        'pending_requests': pending_requests
    }
    return render(request, 'users/follow_requests.html', context)


@login_required
def accept_request(request, follow_id):
    if request.method == 'POST':
        follow_record = get_object_or_404(Follow, id=follow_id, following=request.user, is_accepted=False)
        follow_record.is_accepted = True
        follow_record.save()

    return redirect('users:follow_requests')


@login_required
def reject_request(request, follow_id):
    if request.method == 'POST':
        follow_record = get_object_or_404(Follow, id=follow_id, following=request.user, is_accepted=False)
        follow_record.delete()

    return redirect('users:follow_requests')

@login_required
def follow_list(request, username, follow_type):
    target_user = get_object_or_404(User, username=username)

    can_see = True
    if target_user.is_private and request.user != target_user:
        is_following = Follow.objects.filter(follower=request.user, following=target_user, is_accepted=True).exists()
        if not is_following:
            can_see = False

    if not can_see:
        messages.error(request, "This account is private.")
        return redirect('users:profile', username=username)

    if follow_type == 'followers':
        follows = Follow.objects.filter(following=target_user, is_accepted=True).select_related('follower')
        users_list = [f.follower for f in follows]
        page_title = 'Followers'
    else:
        follows = Follow.objects.filter(follower=target_user, is_accepted=True).select_related('following')
        users_list = [f.following for f in follows]
        page_title = 'Following'

    accepted_following_ids = Follow.objects.filter(follower=request.user, is_accepted=True).values_list('following_id', flat=True)
    pending_following_ids = Follow.objects.filter(follower=request.user, is_accepted=False).values_list('following_id', flat=True)

    context = {
        'target_user': target_user,
        'page_type': page_title,
        'users_list': users_list,
        'accepted_following_ids': accepted_following_ids,
        'pending_following_ids': pending_following_ids,
    }
    return render(request, 'users/follow_list.html', context)


@login_required
@permission_required('users.can_ban_user', raise_exception=True)
def ban_user(request, username):
    if request.method == 'POST':
        user_to_ban = get_object_or_404(User, username=username)

        if user_to_ban.is_superuser:
            messages.error(request, "You cannot ban an administrator.")
        elif user_to_ban == request.user:
            messages.error(request, "You cannot ban yourself.")
        else:
            user_to_ban.is_active = False
            user_to_ban.save()
            messages.success(request, f"User {username} has been successfully banned.")

    return redirect(request.META.get('HTTP_REFERER', 'feed:home'))

