from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)

from .managers import CustomManager
from .utils.utils import get_path_upload_avatar


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model where nickname
    is the unique identifiers for authentication
    """
    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['email']
    GENDERS = (('M', 'Male'), ('F', 'Female'))

    objects = CustomManager()

    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        default='media/user_avatar/default',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])],
    )
    auth_provider     = models.CharField(max_length=255, null=False, default='email')
    about             = models.TextField(max_length=2000, blank=True, null=True)
    birthdate         = models.DateField(help_text='User birthdate', null=True)
    email             = models.EmailField(max_length=150, unique=True, null=False)
    gender            = models.CharField(choices=GENDERS, max_length=10)
    nickname          = models.CharField(max_length=255, unique=True, blank=True)
    name              = models.CharField(max_length=255, blank=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)
    # Permissions
    is_active         = models.BooleanField(default=False)
    is_staff          = models.BooleanField(default=False)
    read_only         = models.BooleanField(default=False)
    # favouires
    favourites_anime  = models.ManyToManyField('anime_db.Anime', related_name='favourites_anime', blank=True)
    favourites_manga  = models.ManyToManyField('manga_db.Manga', related_name='favourites_anime', blank=True)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
