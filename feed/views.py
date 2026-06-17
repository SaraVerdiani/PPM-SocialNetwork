from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView

from posts.models import Post
from posts.views import CommentForm
from users.models import User, Follow


class HomeView(ListView):
    model = Post
    template_name = 'sitecontent/home.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


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
        'comment_form': CommentForm()
    }


    return render(request, 'users/profile.html', context)