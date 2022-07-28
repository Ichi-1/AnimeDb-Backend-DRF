from .utils.services import (
    get_path_upload_avatar,
    validate_size_image,
)
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin
)
from django_countries.fields import CountryField
from django.core.validators import FileExtensionValidator
from django.db import models
from .managers import CustomManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model where nickname 
    is the unique identifiers for authentication
    """
    genders = (('M', 'Male'), ('F', 'Female'))

    email = models.EmailField(max_length=150, unique=True, null=False)
    nickname = models.CharField(max_length=255, unique=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    about = models.TextField(max_length=2000, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png']),
            validate_size_image,
        ]
    )
    birhdate = models.DateTimeField(help_text='User birthday', null=True)
    gender = models.CharField(choices=genders, max_length=10)
    location = CountryField(blank_label='(select country)')
    last_online_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_only = models.BooleanField(default=False)

    # Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = []
    objects = CustomManager()

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    def __str__(self):
        return self.email

    @property
    def is_authenticated(self):
        """
        Always return True
        """
        return True



# class Friend(models.Model):
#     """
#     Friends models
#     """
#     user = models.ForeignKey(
#         AuthUser, on_delete=models.CASCADE, related_name='user'
#     )
#     friend = models.ForeignKey(
#         AuthUser, on_delete=models.CASCADE, related_name='friends'
#     )

#     def __str__(self):
#         return f'{self.friend} is friend with {self.user}'
    

# class SocialLinks(models.Model):
#     """
#     Social links belong to AuthUser
#     """
#     user = models.ForeignKey(
#         AuthUser, on_delete=models.CASCADE, related_name='social_links'
#     )
#     link = models.URLField(max_length=100)

#     def __str__(self):
#         return f'{self.user}'