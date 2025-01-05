from django import forms
from .models import Message, Chat


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


class GroupForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['group_name']
        widgets = {
            'group_name': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'id': 'chatName',
                'name': 'chat_name',
                'placeholder': 'Name...',
                'maxlength': '100',
                'autofocus': True,
                'style': 'border-radius: 20px',
            })
        }
