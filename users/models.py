import random
from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from utils.file_utils import validate_file_size, IMAGE_EXTENSIONS, VIDEO_EXTENSIONS
from django.core.validators import FileExtensionValidator


def upload_to(instance, filename):
    seq = ''.join(map(str, random.sample(range(10), 10)))
    return f'profiles/{instance.username}/{seq}_{filename[-10:]}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True, null=True)
    image = models.ImageField(
        upload_to=upload_to,
        default='default/profile_default.png',
        validators=[
            FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS + VIDEO_EXTENSIONS),
            validate_file_size,
        ]
    )
    banner = models.ImageField(
        upload_to=upload_to,
        default='default/banner.jpg'
    )
    email = models.EmailField(max_length=200, null=True)
    bio = models.TextField(max_length=300, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    # def save(self, *args, **kwargs):
    #     if self.image and self.image.name:
    #         extension = self.file_ext()['ext']
    #         if extension in [ext for ext in IMAGE_EXTENSIONS if ext != 'gif']:
    #             self.file = image_compression(self.file)



    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-created']
