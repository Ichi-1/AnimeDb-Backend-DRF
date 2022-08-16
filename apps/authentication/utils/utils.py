from django.core.exceptions import ValidationError


def get_path_upload_avatar(user, file_name):
    """
    Creating path to user avatars dir.
    Format: f'/media/user_avatar/user_{self.pk}/{file_name}'
    """
    return f'user_avatar/user_{user.id}/{file_name}'


def validate_size_image(file_obj):
    mb_limit = 2
    if file_obj.size > mb_limit * 1024 * 1024:
        raise ValidationError(f'Size limit: {mb_limit} Mb')
