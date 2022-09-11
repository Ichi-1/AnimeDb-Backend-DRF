from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.management.utils import get_random_secret_key
from rest_framework_simplejwt.tokens import RefreshToken
from .utils.utils import silly_username_generator


class CustomManager(BaseUserManager):

    def email_validation(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('You must provide a valid email')

    def create_superuser(self, nickname, email, password=None, **extra_fields):
        if not nickname:
            raise ValueError('Superuser Account: You must provide a nickname')

        email = self.normalize_email(email)
        self.email_validation(email)

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True")

        return self.create_user(nickname, email, password, **extra_fields)

    def create_user(self, nickname, email, password=None, **extra_fields):
        """
        Create a regular User Account with the given email and password.
        """
        if not email:
            raise ValueError('User Account: You must provide a email')

        email = self.normalize_email(email)
        user = self.model(
            nickname=nickname, email=email, is_activte=True, **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_social_user(self, provider, user_data):
        """
        Create a User Account based on social provider data (OAuth2)
        """
        if provider == 'google':
            given_name = user_data['given_name']
            email = user_data['email']
            silly_nickname = silly_username_generator()
            silly_unique_username = f'{silly_nickname} {given_name}'

            social_user = self.create_user(
                nickname=silly_unique_username,
                email=email,
                auth_provider=provider,
                password=get_random_secret_key(),
            )
            social_user.is_active = True
            social_user.save()
            tokens = self.get_tokens(social_user)
            return tokens

        if provider == 'github':
            nickname = user_data['login']
            email = user_data['email']

            social_user = self.create_user(
                nickname=nickname,
                email=email,
                auth_provider=provider,
                password=get_random_secret_key(),
            )
            social_user.is_active = True
            social_user.save()
            tokens = self.get_tokens(social_user)
            return tokens

    @staticmethod
    def get_tokens(user):
        refresh = RefreshToken.for_user(user)

        # Add custom claims
        refresh['nickname'] = user.nickname
        refresh['avatar'] = f'{settings.STORAGE_URL}{user.avatar}'

        update_last_login(None, user=user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
