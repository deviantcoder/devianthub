import utils.file_utils as utils
from django.db import models
from uuid import uuid4
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from users.models import Profile
from mptt.models import MPTTModel, TreeForeignKey
from utils.content_utils import time_since_obj_posted


class Post(models.Model):
    POST_TYPE = (
        ('text', 'Text'),
        ('media', 'Media'),
        ('link', 'Link')
    )

    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    # community
    title = models.CharField(max_length=100)
    body = models.TextField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)

    draft = models.BooleanField(default=False, null=True, blank=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPE, default='text', null=True)

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

    def updated_status(self):
        if self.updated and (self.updated.hour != self.created.hour or self.updated.minute != self.created.minute):
            updated_time = timezone.localtime(self.updated)
            return f"(updated on: {updated_time.strftime('%b. %d, %I:%M %p')})"
        return False

    def time_since_posted(self):
        return time_since_obj_posted(self)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']


def upload_to(instance, filename):
    return f'posts/{instance.post.id}/{filename}'


class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=upload_to,
        validators=[
            FileExtensionValidator(allowed_extensions=utils.IMAGE_EXTENSIONS + utils.VIDEO_EXTENSIONS),
            utils.validate_file_size,
        ]
    )

    created = models.DateTimeField(auto_now_add=True, null=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def file_ext(self):
        return utils.get_file_extension(self.file, file_type=True)

    def save(self, *args, **kwargs):
        if self.file and self.file_ext()['ext'] not in utils.VIDEO_EXTENSIONS:
            self.file = utils.image_compression(self.file)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.post.title}_{self.file.name}'
    
    class Meta:
        ordering = ['post', 'created']


class PostStats(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    upvotes = models.PositiveIntegerField(default=0, blank=True)
    downvotes = models.PositiveIntegerField(default=0, blank=True)
    comments = models.PositiveIntegerField(default=0, blank=True)
    reposts = models.PositiveIntegerField(default=0, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.post.title
    
    @property
    def votes(self):
        votes_ratio = self.upvotes - self.downvotes
        return votes_ratio if votes_ratio else 0

    class Meta:
        ordering = ['post']
        verbose_name = 'Post statistics'
        verbose_name_plural = 'Post stats'


class VotePost(models.Model):
    VOTES_TYPES = (
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    )


    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

    vote_type = models.CharField(max_length=10, choices=VOTES_TYPES, null=True)
    
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        unique_together = ('post', 'user')
        verbose_name = 'Post Vote'
        verbose_name_plural = 'Post Votes'
        ordering = ['post', 'vote_type', 'created']
    
    def __str__(self):
        return f'{self.vote_type}: {self.post.id}'


class Comment(MPTTModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

    body = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def time_since_posted(self):
        return time_since_obj_posted(self)

    class MPTTMeta:
        order_insertion_by = ['post']

    def __str__(self):
        return self.user.username


class CommentStats(models.Model):
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE)
    upvotes = models.PositiveIntegerField(default=0, blank=True)
    downvotes = models.PositiveIntegerField(default=0, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.comment.user.username

    @property
    def votes(self):
        votes_ratio = self.upvotes - self.downvotes
        return votes_ratio if votes_ratio else 0

    class Meta:
        ordering = ['comment']
        verbose_name = 'Comment statistics'
        verbose_name_plural = 'Comment stats'


class VoteComment(models.Model):
    VOTES_TYPES = (
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    )

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

    vote_type = models.CharField(max_length=10, choices=VOTES_TYPES)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        unique_together = ('comment', 'user')
        verbose_name = 'Comment Vote'
        verbose_name_plural = 'Comment Votes'
        ordering = ['comment', 'vote_type', 'created']


    def __str__(self):
        return f'{self.vote_type}: {self.comment.id}'
