import requests
from django.conf import settings

AUTH_URL = 'https://github.com/login/oauth/access_token'
API_URL = 'https://api.github.com/user'

class GitHubService:

    @staticmethod
    def get_access_token(code):
        data = {
            'client_id': settings.GITHUB_OAUTH_CLIENT_ID,
            'client_secret': settings.GITHUB_OAUTH_CLIENT_SECRET,
            'code': code
        }
        headers = {
            'Accept': 'application/json'
        }
        response = requests.post(AUTH_URL, data=data, headers=headers)

        """
        Return only token.
        Also contain: token type', 'scope'
        """
        return response.json()


    @staticmethod
    def get_user_info(access_token):
        headers = {
            'Authorization': f'token {access_token}',
        }
        response = requests.post(API_URL, headers=headers)
        return response.json()

        

