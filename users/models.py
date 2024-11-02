import random
from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


def upload_to(instance, filename):
    seq = ''.join(map(str, random.sample(range(10), 10)))
    return f'profiles/{instance.username}/{filename[:10]}_{seq}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True, null=True)
    image = models.ImageField(
        upload_to=upload_to,
        default='../img/profile_default.png'
    )
    banner = models.ImageField(
        upload_to=upload_to,
        default='../img/banner.jpg'
    )
    email = models.EmailField(max_length=200, unique=True, null=True)
    bio = models.CharField(max_length=500, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-created']
