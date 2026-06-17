from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from users.models import User
from .models import Post, Comment

from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description']

        labels = {
            'description': '',
        }

        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'border-0 shadow-none custom-textarea',
                'rows': 6,
                'placeholder': 'Describe your post',
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control rounded-pill bg-light border-0',
                'placeholder': 'Write your comment...',
                'autocomplete': 'off'
            })
        }

        labels = {
            'text': ''
        }



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)

            new_post.author = request.user

            new_post.save()

            return redirect('feed:home')
    else:
        form = PostForm()

    return render(request, 'sitecontent/create_post.html', {'form': form})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.author and request.method == 'POST':
        post.delete()

    return redirect(request.META.get('HTTP_REFERER', 'feed:home'))


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.author and request.method == 'POST':
        comment.delete()

    return redirect(request.META.get('HTTP_REFERER', 'feed:home'))

