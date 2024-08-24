from django.db import models
from uuid import uuid4
from .validators import validate_file_size
from django.core.validators import FileExtensionValidator
from django.utils import timezone


class Post(models.Model):
    # user
    # community
    title = models.CharField(max_length=100)
    body = models.TextField(null=True, blank=True)

    video_url = models.URLField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    # returns 1 if post has one file, 2 if multiple and False if none
    def has_media_files(self):
        if self.postmedia_set.all().exists():
            if self.postmedia_set.all().count() == 1:
                return 1
            return 2
        return False
    
    def time_since_posted(self):
        time_diff = timezone.now() - self.created
        time_diff = time_diff.total_seconds() // 3600
        return int(time_diff)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']


def upload_to(instance, filename):
    return f'{instance.post.title}_{str(instance.post.id)[:10]}/{filename}'


class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=upload_to,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov']),
            validate_file_size,
        ]
    )

    def __str__(self):
        return f'{self.post.title}_{self.file.name}'
    
    class Meta:
        ordering = ['post']