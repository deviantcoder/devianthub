from django import forms
from .models import Post, PostMedia, Comment
from django.forms import inlineformset_factory
from mptt.forms import TreeNodeChoiceField


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'body', 'video_url',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control login-field', 'placeholder': 'Enter your post title', 'type': 'text', 'title': 'title'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control login-field', 'placeholder': 'Write your post here...', 'name': 'body', 'rows': 4, 
                'style': 'resize: vertical; min-height: 50px;'
            }),
            'video_url': forms.TextInput(attrs={
                'class': 'form-control login-field post-creation-field', 'placeholder': 'YouTube video link', 'type': 'text', 'name': 'video_url'
            }),
        }
        labels = {
            'title': 'Title',
            'body': 'Body',
            'video_url': 'YouTube video link'
        }


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


class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update({'class': 'is-hidden'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ['parent', 'body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control login-field', 'placeholder': 'Write your comment here...', 'name': 'body', 'rows': 4,
                'style': 'resize: vertical; height: 50px; min-height: 50px; max-height: 200px;'
            })
        }
