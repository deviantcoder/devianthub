from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile, UserActivityStats


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            display_name=user.username,
            email=user.email if user.email else ''
        )


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except User.DoesNotExist:
        pass


@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, *args, **kwargs):
    if not created:
        profile = instance
        user = profile.user
        user.username = profile.username
        user.save()


@receiver(post_save, sender=Profile)
def create_user_activity_stats(sender, instance, created, **kwargs):
    if created:
        stats = UserActivityStats.objects.create(
            profile=instance
        )