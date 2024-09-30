import os
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from .models import PostMedia, Post

post_delete_flag = False

@receiver(pre_delete, sender=PostMedia)
def delete_post_media_file(sender, instance, **kwargs):
    if not post_delete_flag:
        if instance.file:
            instance.file.delete()


@receiver(post_delete, sender=Post)
def delete_post_media(sender, instance, **kwargs):
    global post_delete_flag
    post_delete_flag = True

    post_media = instance.postmedia_set.all()

    if post_media.exists():
        media_dir = os.path.dirname(post_media.first().file.path)

        for media in post_media:
            media.file.delete()

        if os.path.exists(media_dir):
            os.rmdir(media_dir)
    
    post_delete_flag = False