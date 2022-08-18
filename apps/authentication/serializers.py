from rest_framework import serializers
from apps.authentication.models import CustomUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserCreateSerializer


class SignUpSerializer(UserCreateSerializer):
    """
    Used in Djoser as custom serializer
    """

    class Meta:
        model = CustomUser
        fields = ('nickname', 'email', 'password')

    nickname = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        min_length=6
    )
