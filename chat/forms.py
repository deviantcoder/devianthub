from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']

        widgets = {
            'body': forms.TextInput({
                'class': 'form-control me-2',
                'type': 'text',
                'placeholder': 'Type a message...',
            })
        }