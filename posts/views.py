
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Comment
from django.views.generic import DetailView
from django.urls import reverse
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

    referer = request.META.get('HTTP_REFERER', '/')

    if f"/{post_id}/" in referer:
        return redirect('users:profile', username=request.user.username)

    return redirect(referer)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.author and request.method == 'POST':
        comment.delete()

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

def pin_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    post.is_pinned = not post.is_pinned
    post.save()

    return redirect(request.META.get('HTTP_REFERER', 'users:profile'))