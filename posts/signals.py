# import os
# from django.db.models.signals import pre_delete, post_delete
# from django.dispatch import receiver
# from .models import PostMedia, Post

# post_delete_flag = False

# @receiver(pre_delete, sender=Post)
# def media_dir(sender, instance, **kwargs):
#     instance._media_files = list(instance.postmedia_set.all())

#     if instance._media_files:
#         instance._media_dir = os.path.dirname(instance._media_files[0].file.path)


# @receiver(post_delete, sender=Post)
# def delete_post_media(sender, instance, **kwargs):
#     global post_delete_flag
#     post_delete_flag = True

#     for media in instance._media_files:
#         media.file.delete()
    
#     if hasattr(instance, '_media_dir') and os.path.exists(instance._media_dir):
#         os.rmdir(instance._media_dir)
    
#     post_delete_flag = False


# @receiver(pre_delete, sender=PostMedia)
# def delete_post_media_file(sender, instance, **kwargs):
#     if not post_delete_flag and instance.file:
#             instance.file.delete()


import os
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from .models import PostMedia, Post


@receiver(pre_delete, sender=Post)
def delete_post_media(sender, instance, **kwargs):
    post = instance

    if post.postmedia_set.all():
        dir_path = os.path.dirname(post.postmedia_set.first().file.path)

        for media in post.postmedia_set.all():
            if media:
                media.file.delete()

        if os.path.exists(dir_path):
            os.rmdir(dir_path)