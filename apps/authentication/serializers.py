from apps.users.models import User
from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers as s
from rest_framework.validators import UniqueValidator


class SignUpSerializer(UserCreateSerializer):
    """
    Used in Djoser as custom serializer
    """
    class Meta:
        model = User
        fields = ('nickname', 'email', 'password')

    nickname = s.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = s.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = s.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        min_length=6
    )


class GoogleLoginSerializer(s.Serializer):
    id_token = s.CharField()


class GitHubLoginSerializer(s.Serializer):
    code = s.CharField()
