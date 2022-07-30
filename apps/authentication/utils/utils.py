from django.core.exceptions import ValidationError


def get_path_upload_avatar(user, file_name):
    """
    Creating path to user avatars dir.
    Format: /media/avatar/user_id/photo.img
    """

    return f'avatar/{user.id}/{file_name}'


def validate_size_image(file_obj):
    mb_limit = 2
    if file_obj.size > mb_limit * 1024 * 1024:
        raise ValidationError(f'Size limit: {mb_limit} Mb')
