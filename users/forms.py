from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


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
            'placeholder': 'Username'
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
        return username.lower() if username else username


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'image',
            'banner',
            'bio',
        ]