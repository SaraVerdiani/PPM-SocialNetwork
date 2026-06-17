from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView

from posts.models import Post
from users.models import User, Follow


class HomeView(ListView):
    model = Post
    template_name = 'sitecontent/home.html'
    context_object_name = 'posts'


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_posts = profile_user.posts.all()

    is_following = False
    if request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    context = {
        'profile_user': profile_user,
        'posts': user_posts,
        'is_following': is_following,
        'followers_count': profile_user.following.count(),
        'following_count': profile_user.follower.count(),
    }


    return render(request, 'users/profile.html', context)