from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from posts.models import Post, News
from posts.views import CommentForm
from users.models import User, Follow


class HomeView(ListView):
    model = Post
    template_name = 'sitecontent/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = self.request.user

        base_qs = Post.objects.select_related('author').prefetch_related('likes', 'comments')

        if not user.is_authenticated:
            return base_qs.filter(author__is_private=False).order_by('-created_at')

        followed_users_ids = Follow.objects.filter(
            follower=user,
            is_accepted=True
        ).values_list('following_id', flat=True)

        queryset = Post.objects.filter(author__is_active = True).filter(
            Q(author__is_private=False) |
            Q(author=user) |
            Q(author__in=followed_users_ids)
        ).distinct().order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)

    is_following = False
    follow_request_pending = False

    if request.user != profile_user:
        follow_record = Follow.objects.filter(follower=request.user, following=profile_user).first()
        if follow_record:
            is_following = follow_record.is_accepted
            follow_request_pending = not follow_record.is_accepted

    can_see_posts = True
    if profile_user.is_private and request.user != profile_user and not is_following:
        can_see_posts = False

    pinned_posts = []
    posts = []

    if can_see_posts:
        base_posts = Post.objects.filter(author=profile_user) \
            .select_related('author') \
            .prefetch_related('likes', 'comments') \
            .order_by('-created_at')

        pinned_posts = base_posts.filter(is_pinned=True)
        posts = base_posts.filter(is_pinned=False)

    followers_count = Follow.objects.filter(following=profile_user, is_accepted=True).count()
    following_count = Follow.objects.filter(follower=profile_user, is_accepted=True).count()

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'pinned_posts': pinned_posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
        'comment_form': CommentForm(),
        'follow_request_pending': follow_request_pending,
        'can_see_posts': can_see_posts,
    }

    return render(request, 'users/profile.html', context)


class ExploreView(TemplateView):
    template_name = 'sitecontent/explore.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        base_suggested_users = User.objects.filter(is_active=True).exclude(is_superuser=True)

        if user.is_authenticated:
            context['suggested_users'] = base_suggested_users.exclude(id=user.id).order_by('-date_joined')[:4]

            context['accepted_following_ids'] = set(Follow.objects.filter(
                follower=user,
                is_accepted=True
            ).values_list('following_id', flat=True))

            context['pending_following_ids'] = set(Follow.objects.filter(
                follower=user,
                is_accepted=False
            ).values_list('following_id', flat=True))

        else:
            context['suggested_users'] = base_suggested_users.order_by('-date_joined')[:4]
            context['accepted_following_ids'] = set()
            context['pending_following_ids'] = set()

        context['news_items'] = News.objects.all().order_by('-created_at')[:6]

        return context