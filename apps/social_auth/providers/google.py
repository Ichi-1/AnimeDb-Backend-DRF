from google.auth.transport.requests import Request
from google.oauth2 import id_token
from django.conf import settings
from django.core.exceptions import ValidationError


class GoogleService:
    
    @staticmethod
    def validate_id_token(auth_token):
        try:
            id_info = id_token.verify_oauth2_token(auth_token, Request())
            audience = id_info['aud']
            if audience != settings.GOOGLE_OAUTH2_CLIEN_ID:
                raise ValidationError('id_token is invalid') 
            return id_info
        except:
            return False
        
        