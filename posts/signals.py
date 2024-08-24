from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import PostMedia


@receiver(pre_delete, sender=PostMedia)
def delete_post_media(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete()