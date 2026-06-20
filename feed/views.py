from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView

from posts.models import Post, News
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
    
    pinned_posts = Post.objects.filter(author=profile_user, is_pinned=True).order_by('-created_at')

    regular_posts = Post.objects.filter(author=profile_user, is_pinned=False).order_by('-created_at')

    is_following = False
    if request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    context = {
        'profile_user': profile_user,
        'posts': regular_posts,
        'pinned_posts': pinned_posts,
        'is_following': is_following,
        'followers_count': profile_user.following.count(),
        'following_count': profile_user.follower.count(),
        'comment_form': CommentForm()
    }


    return render(request, 'users/profile.html', context)


class ExploreView(TemplateView):
    template_name = 'sitecontent/explore.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['suggested_users'] = User.objects.exclude(id=self.request.user.id).exclude(is_superuser=True)[:4]
            context['followed_users_ids'] = Follow.objects.filter(follower=self.request.user).values_list('following_id', flat=True)
        else:
            context['suggested_users'] = User.objects.exclude(is_superuser=True)[:4]
            context['followed_users_ids'] = []

        context['news_items'] = News.objects.all().order_by('-created_at')[:6]

        return context