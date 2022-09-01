from apps.authentication.models import User
from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class SignUpSerializer(UserCreateSerializer):
    """
    Used in Djoser as custom serializer
    """

    nickname = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        min_length=6
    )

    class Meta:
        model = User
        fields = ('nickname', 'email', 'password')


class GoogleLoginSerializer(serializers.Serializer):
    id_token = serializers.CharField()


class GitHubLoginSerializer(serializers.Serializer):
    code = serializers.CharField()
