import random
import utils.file_utils as utils
from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from django.core.validators import FileExtensionValidator
from django.core.files.storage import default_storage


def upload_to(instance, filename):
    seq = ''.join(map(str, random.sample(range(10), 10)))
    return f'profiles/{instance.username}/{seq}_{filename[-10:]}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=15, unique=True, null=True)
    display_name = models.CharField(max_length=15, null=True, blank=True)

    image = models.ImageField(
        upload_to=upload_to,
        default='default/profile_default.png',
        validators=[
            FileExtensionValidator(allowed_extensions=tuple(ext for ext in utils.IMAGE_EXTENSIONS if ext != 'gif')),
            utils.validate_file_size,
        ]
    )
    banner = models.ImageField(
        upload_to=upload_to,
        default='default/banner.jpg',
        validators=[
            FileExtensionValidator(allowed_extensions=tuple(ext for ext in utils.IMAGE_EXTENSIONS if ext != 'gif')),
            utils.validate_file_size,
        ]
    )
    email = models.EmailField(max_length=100, null=True)
    bio = models.TextField(max_length=300, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def file_ext(self):
        return {
            'image': utils.get_file_extension(self.image),
            'banner': utils.get_file_extension(self.banner),
        }

    def get_username(self):
        return self.display_name if self.display_name else self.username

    def save(self, *args, **kwargs):
        old_files = {'image': None, 'banner': None}

        if Profile.objects.filter(id=self.id).exists():
            profile = Profile.objects.get(id=self.id)
            old_files['image'] = profile.image.path if profile.image else None
            old_files['banner'] = profile.banner.path if profile.banner else None

        for field in ['image', 'banner']:
            file = getattr(self, field)
            if file and file.name:
                compressed_file = utils.image_compression(file)
                setattr(self, field, compressed_file)

        super().save(*args, **kwargs)

        for field, old_path in old_files.items():
            new_file = getattr(self, field)
            if old_path and old_path != new_file.path:
                if default_storage.exists(old_path):
                    default_storage.delete(old_path)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-created']
