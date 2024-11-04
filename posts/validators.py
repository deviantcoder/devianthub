# from django.core.exceptions import ValidationError
#
#
# def validate_file_size(file):
#     IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif')
#     VIDEO_EXTENSIONS = ('.mp4', '.mov', '.avi')
#     LIMIT_SIZE_LIMIT = 17
#     VIDEO_SIZE_LIMIT = 100
#
#     file_size = file.size / (1024 ** 2)
#
#     if file.name.lower().endswith(IMAGE_EXTENSIONS) and file_size > LIMIT_SIZE_LIMIT:
#         raise ValidationError(f'Image size should not exceed {LIMIT_SIZE_LIMIT} MB.')
#     elif file.name.lower().endswith(VIDEO_EXTENSIONS) and file_size > VIDEO_SIZE_LIMIT:
#         raise ValidationError(f'Video size should not exceed {VIDEO_SIZE_LIMIT} MB.')