from apps.authentication.models import CustomUser
from apps.authentication.utils.tokens import get_tokens_for_user
from django.core.management.utils import get_random_secret_key
from .utils import silly_username_generator


def create_social_account(provider, user_data):

    if provider == 'google':
        given_name = user_data['given_name']
        email = user_data['email']
        silly_nickname = silly_username_generator()
        silly_unique_username = f'{silly_nickname} {given_name}'

        social_user = CustomUser.objects.create_user(
            nickname=silly_unique_username,
            email=email,
            auth_provider=provider,
            password=get_random_secret_key(),
        )
        social_user.is_active = True
        social_user.save()
        tokens = get_tokens_for_user(social_user)
        return tokens

    
    if provider == 'github':
        nickname = user_data['login']
        email = user_data['email']
        
        social_user = CustomUser.objects.create_user(
            nickname=nickname,
            email=email,
            auth_provider=provider,
            password=get_random_secret_key(),
        )
        social_user.is_active = True
        social_user.save()
        tokens = get_tokens_for_user(social_user)
        return tokens
        


def grant_access_social_account(social_user):
    tokens = get_tokens_for_user(social_user)
    return tokens
