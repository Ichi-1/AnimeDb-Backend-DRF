
def get_path_upload_avatar(user, file_name):
    """
    Creating path to user avatars dir.
    Format: f'/media/user_avatar/user_{self.pk}/{file_name}'
    """
    return f'user_avatar/user_{user.id}/{file_name}'

