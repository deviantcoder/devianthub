from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'input round-corners-medium is-medium',
            'placeholder': 'Username',
            'name': 'username',
            'id': 'username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'input round-corners-medium is-medium',
            'placeholder': 'Email'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'input round-corners-medium is-medium',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'input round-corners-medium is-medium',
            'placeholder': 'Repeat password'
        })

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username and User.objects.filter(username=username).exists():
            raise ValidationError('Username already taken.')

        return username.lower() if username else username


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'username',
            'bio',
            'image',
            'banner',
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input round-corners-small is-medium',
                'placeholder': 'Username',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'input round-corners-small is-medium',
                'placeholder': 'Bio',
                'style': 'resize: vertical; min-height: 135px; max-height: 135px;'
            }),
            'image': forms.FileInput(attrs={
                'class': 'input is-small',
                'placeholder': 'Image',
            }),
            'banner': forms.FileInput(attrs={
                'class': 'input is-small',
                'placeholder': 'Banner',
            })
        }