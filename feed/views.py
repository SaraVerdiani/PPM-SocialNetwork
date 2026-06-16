from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView

from posts.models import Post
from users.models import User


class HomeView(ListView):
    model = Post
    template_name = 'sitecontent/home.html'
    context_object_name = 'posts'


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)

    user_posts = profile_user.posts.all()

    context = {
        'profile_user': profile_user,
        'posts': user_posts
    }

    return render(request, 'users/profile.html', context)