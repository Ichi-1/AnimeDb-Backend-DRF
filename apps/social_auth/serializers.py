import os
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .providers.google import GoogleService
from .services import create_social_account


class GoogleAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = GoogleService.validate(auth_token)
        print(user_data)
    
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'Token is invalid or expired'
            )
        
        #! BUGS START HERE. TOKEN IS OBTAINED 
        # if user_data['aud'] != os.environ.get('GOOGLE_OAUTH2_CLIEN_ID'):
        #     raise AuthenticationFailed('Authentication failed')

        user_id = user_data['sub']
        email = user_data['email']
        nickname = user_data['nickname']
        provider = 'google'

        return create_social_account(
            provider=provider,
            user_id=user_id,
            nickname=nickname,
            email=email,
        )
            
            