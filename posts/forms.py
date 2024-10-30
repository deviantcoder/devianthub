from django import forms
from .models import Post, PostMedia
from django.forms import inlineformset_factory, BaseFormSet


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'body', 'video_url',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input post-creation-field', 'placeholder': 'Enter your post title', 'type': 'text', 'title': 'title'
            }),
            'body': forms.Textarea(attrs={
                'class': 'textarea post-creation-field', 'placeholder': 'Write your post here...', 'name': 'body', 'rows': 4, 
                'style': 'resize: vertical; min-height: 50px;'
            }),
            'video_url': forms.TextInput(attrs={
                'class': 'input post-creation-field', 'placeholder': 'YouTube video link', 'type': 'text', 'name': 'video_url'
            }),
        }
        labels = {
            'title': 'Title',
            'body': 'Body',
            'video_url': 'YouTube video link'
        }

    # def __init__(self, *args, **kwargs):
    #     post_type = kwargs.pop('post_type', None)
    #     super().__init__(*args, **kwargs)

    #     if post_type == 'text':
    #         self.fields['video_url'].widget = forms.HiddenInput()
    #     elif post_type == 'media':
    #         self.fields['video_url'].widget = forms.HiddenInput()

class PostMediaForm(forms.ModelForm):
    class Meta:
        model = PostMedia
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'accept': 'image/*',
                'class': 'browse-files-button'
            }),
        }


PostMediaFormSet = inlineformset_factory(
    Post, PostMedia, form=PostMediaForm, extra=0, can_delete=True
)