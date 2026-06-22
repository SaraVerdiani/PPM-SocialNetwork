from django import forms

from posts.models import Post, Comment


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

