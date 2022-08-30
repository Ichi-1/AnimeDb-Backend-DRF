from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from .managers import CustomManager
from .utils.utils import get_path_upload_avatar


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model where nickname
    is the unique identifiers for authentication
    """
    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['email']
    GENDERS = (('M', 'Male'), ('F', 'Female'))

    email      = models.EmailField(max_length=150, unique=True, null=False)
    nickname   = models.CharField(max_length=255, unique=True, blank=True)
    name       = models.CharField(max_length=255, blank=True)
    avatar     = models.ImageField(
        upload_to=get_path_upload_avatar,
        default='media/user_avatar/default',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])],
    )
    about      = models.TextField(max_length=2000, blank=True, null=True)
    birthdate  = models.DateField(help_text='User birthdate', null=True)
    gender     = models.CharField(choices=GENDERS, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_only  = models.BooleanField(default=False)
    # Permissions
    is_active  = models.BooleanField(default=False)
    is_staff   = models.BooleanField(default=False)
    auth_provider = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        default='email'
    )
    objects = CustomManager()

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
