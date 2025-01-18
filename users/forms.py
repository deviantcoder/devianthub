from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, SocialLink
from django.core.exceptions import ValidationError

from allauth.account.forms import LoginForm, SignupForm


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
            'class': 'form-control login-field',
            'placeholder': 'Username',
            'name': 'username',
            'id': 'username',
            'maxlength': '15',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control login-field',
            'placeholder': 'Email'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control login-field',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control login-field',
            'placeholder': 'Confirm password'
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
            'display_name',
            'bio',
            'image',
            'banner',
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control login-field',
                'placeholder': 'Username',
                'name': 'username',
                'id': 'username',
            }),
            'display_name': forms.TextInput(attrs={
                'class': 'form-control login-field',
                'placeholder': 'Display Name',
                'name': 'display_name',
                'id': 'display_name',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control login-field',
                'placeholder': 'Write something about yourself...',
                'style': 'resize: vertical; min-height: 243px; max-height: 243px; font-size: 17px;',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control login-field',
                'placeholder': 'Image',
                'name': 'image',
            }),
            'banner': forms.FileInput(attrs={
                'class': 'form-control login-field',
                'placeholder': 'Banner',
                'name': 'banner',
            })
        }


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'password':
                field.widget.attrs.update({
                    'type': 'password',
                    'name': 'password',
                    'class': 'form-control login-field',
                    'id': 'password',
                    'placeholder': 'Enter a password',
                })
            elif name == 'login':
                field.widget.attrs.update({
                    'type': 'text',
                    'name': 'username',
                    'class': 'form-control login-field',
                    'id': 'username',
                    'placeholder': 'Enter username',
                })


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control login-field',
            })


class SocialForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['network', 'url']
