
def get_path_upload_screenshot(screenshot, file_name):
    """
    Creating path to user avatars dir.
    Format: f'anime/{screenshot.anime.title}/{file_name}'
    """
    return f'anime/{screenshot.anime.title}/{file_name}'
