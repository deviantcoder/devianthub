import os
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import PostMedia, Post, PostStats, Comment, CommentStats


@receiver(post_save, sender=Post)
def create_poststats(sender, instance, created, **kwargs):
    if created:
        post_stats = PostStats.objects.create(
            post=instance
        )


@receiver(post_save, sender=Comment)
def create_commentstats(sender, instance, created, **kwargs):
    if created:
        comments_stats = CommentStats.objects.create(
            comment=instance
        )


@receiver(pre_delete, sender=PostMedia)
def delete_post_file(sender, instance, **kwargs):
    if instance.file and instance.file.path and os.path.exists(instance.file.path):
        instance.file.delete()