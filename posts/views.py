from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from users.models import User
from .models import Post

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

