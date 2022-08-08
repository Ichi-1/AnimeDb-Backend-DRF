import os
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from apps.authentication.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken




def create_social_account(provider, user_id, nickname, email):
    candidate = CustomUser.objects.filter(nickname=nickname)
    tokens = RefreshToken.for_user(user_id)

    if candidate.exists():

        if provider == candidate[0].auth_provider:
            new_user = authenticate(
                nickname=nickname,
                password=os.environ.get('SECRET_KEY')
            )
        
            return {
                'nickname': new_user.nickname,
                'email': new_user.email,
                'tokens': tokens
            }
        
        else:
            raise AuthenticationFailed(
                detail='Please continue your login using '.format(candidate[0].auth_provider)
            )
    
    else:
        new_user = CustomUser.objects.create_user(
            nickname=nickname,
            email=email,
            password=os.environ.get('SECRET_KEY')
        )
        new_user.is_active = True
        new_user.auth_provider = provider
        new_user.save()
        authenticate(
            nickname=nickname,
            email=email,
            password=os.environ.get('SECRET_KEY')
        )

        return {
            "nickname": nickname,
            "email": email,
            "tokens": tokens
        }
        
