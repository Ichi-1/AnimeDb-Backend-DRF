
from google.auth.transport.requests import Request
from google.oauth2 import id_token



class GoogleService:
    
    @staticmethod
    def validate(auth_token):
        try:
            id_info = id_token.verify_oauth2_token(
                auth_token, Request()
            )
            if 'https://accounts.google.com' in id_info['iss']:
                return id_info
        except:
            return 'Token invalid or expired'


