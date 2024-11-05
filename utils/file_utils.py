import os
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.core.exceptions import ValidationError


IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif')
VIDEO_EXTENSIONS = ('mp4', 'mov', 'avi')
LIMIT_SIZE_LIMIT = 15
VIDEO_SIZE_LIMIT = 100


def validate_file_size(file):
    file_size = file.size / (1024 ** 2)

    if file.name.lower().endswith(IMAGE_EXTENSIONS) and file_size > LIMIT_SIZE_LIMIT:
        raise ValidationError(f'Image size should not exceed {LIMIT_SIZE_LIMIT} MB.')
    elif file.name.lower().endswith(VIDEO_EXTENSIONS) and file_size > VIDEO_SIZE_LIMIT:
        raise ValidationError(f'Video size should not exceed {VIDEO_SIZE_LIMIT} MB.')

def image_compression(file):
    with Image.open(file) as img:
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=50, optimize=True)
        img_io.seek(0)
        return File(img_io, name=file.name)

def get_file_extension(file, file_type=False):
    _, file_ext = os.path.splitext(file.name)
    if file_type:
        if file_ext.strip('.') in IMAGE_EXTENSIONS:
            return {
                'type': 'image',
                'ext': file_ext.lstrip('.')
            }
        return {
            'type': 'video',
            'ext': file_ext.lstrip('.')
        }

    return file_ext.strip('.')
