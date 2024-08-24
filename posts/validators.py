from django.core.exceptions import ValidationError


def validate_file_size(file):
    limit_mb_image = 10
    limit_mb_video = 100

    image_extensions = ('.jpg', '.jpeg', '.png', '.gif')
    video_extensions = ('.mp4', '.mov', '.avi')

    file_size = file.size / (1024 * 1024)

    if file.name.lower().endswith(image_extensions) and file_size > limit_mb_image:
        raise ValidationError(f'Image size should not exceed {limit_mb_image} MB.')
    elif file.name.lower().endswith(video_extensions) and file_size > limit_mb_video:
        raise ValidationError(f'Video size should not exceed {limit_mb_video} MB.')