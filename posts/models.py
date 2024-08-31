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

    draft = models.BooleanField(default=False, null=True, blank=True)

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
        time_diff = time_diff.total_seconds() / 3600

        week_hours = 24 * 7
        month_hours = 24 * 30

        data = {'type': '', 'num': 0}

        if time_diff < 1 / 60:
            data['type'] = 'now'
        elif time_diff < 1:
            data['type'] = 'minute'
            data['num'] = int(time_diff * 60)             # minutes
        elif time_diff < 24:
            data['type'] = 'hour'
            data['num'] = int(time_diff)                  # hours
        elif 24 <= time_diff < week_hours:
            data['type'] = 'day'
            data['num'] = int(time_diff // 24)            # days
        elif week_hours <= time_diff < month_hours:
            data['type'] = 'week'
            data['num'] = int(time_diff / 24 / 7)         # weeks
        elif time_diff >= month_hours:
            data['type'] = 'month'
            data['num'] = int(time_diff / 24 / 30)        # months 

        return data

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
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.post.title}_{self.file.name}'
    
    class Meta:
        ordering = ['-post']