import os
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from .models import PostMedia, Post


# @receiver(pre_delete, sender=Post)
# def post_files_dir(sender, instance, **kwargs):
#     instance._media_files = [media.file.path for media in instance.postmedia_set.all() if media.file]

#     if instance._media_files:
#         instance._media_dir = os.path.dirname(instance._media_files[0])
#         print(f'\t\t****** MEDIA DIR: {instance._media_dir} ******')


# @receiver(post_delete, sender=Post)
# def delete_post_media(sender, instance, **kwargs):
#     if hasattr(instance, '_media_files'):
#         print(f'\t\t ***** MEDIA FILES: {instance._media_files} *****')
#         print(f'\t\t ***** MEDIA DIR: {instance._media_dir} *****')
#         for file_path in instance._media_files:
#             if os.path.exists(file_path):
#                 os.remove(file_path)
    
#     if hasattr(instance, '_media_dir') and os.path.exists(instance._media_dir):
#         os.rmdir(instance._media_dir)


@receiver(pre_delete, sender=PostMedia)
def delete_post_file(sender, instance, **kwargs):
    if instance.file and instance.file.path and os.path.exists(instance.file.path):
        instance.file.delete()