from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User

class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio', 'is_private']
        labels = {
            'bio': 'Your biography',
            'is_private': 'Make profile private',
        }
        help_texts = {
            'bio': 'Max. 200 characters',
            'is_private': 'If enabled, only approved followers can see your posts.'
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Insert your bio...'})
        }
