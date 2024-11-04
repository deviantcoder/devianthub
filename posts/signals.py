import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import PostMedia


@receiver(pre_delete, sender=PostMedia)
def delete_post_file(sender, instance, **kwargs):
    if instance.file and instance.file.path and os.path.exists(instance.file.path):
        instance.file.delete()