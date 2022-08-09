from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.base_user import BaseUserManager


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
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('User Account: You must provide a email')

        email = self.normalize_email(email)
        user = self.model(nickname=nickname, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
