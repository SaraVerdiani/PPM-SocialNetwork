from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.views.generic import DetailView
from django.urls import reverse
from .models import Post

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, 'Post created successfully')
            return redirect('feed:home')
    else:
        form = PostForm()

    return render(request, 'sitecontent/create_post.html', {'form': form})


@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.author or request.user.has_perm('users.can_delete_post'):
        post.delete()
        messages.success(request, 'Post deleted successfully')
    else:
        raise PermissionDenied

    referer = request.META.get('HTTP_REFERER', '/')
    if f"/{post_id}/" in referer:
        return redirect('users:profile', username=request.user.username)

    return redirect(referer)


@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.author or request.user.has_perm('users.can_delete_comment'):
        comment.delete()
        messages.success(request, 'Comment deleted successfully')
    else:
        raise PermissionDenied

    return redirect(request.META.get('HTTP_REFERER', 'feed:home'))

class PostDetailView(DetailView):
    model = Post
    template_name = 'sitecontent/post_details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()

        referer = self.request.META.get('HTTP_REFERER')

        if referer and '/posts/' not in referer:
            self.request.session['post_back_url'] = referer

        context['back_url'] = self.request.session.get(
            'post_back_url',
            reverse('users:profile', kwargs={'username': self.object.author.username})
        )

        return context
@login_required
@require_POST
def pin_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    post.is_pinned = not post.is_pinned
    post.save()

    return redirect(request.META.get('HTTP_REFERER', 'users:profile'))