from rest_framework import serializers
from apps.authentication.models import User
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


class UserListSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'nickname',
            'avatar_url',
            'last_login',
            'created_at',
        )

    @extend_schema_field(OpenApiTypes.URI)
    def get_avatar_url(self, user: dict) -> str:
        if user.avatar:
            return user.avatar.url
        else:
            return "No image assigned to object"


class UserMeRetrieveSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.URI)
    def get_avatar_url(self, user: dict) -> str:
        if user.avatar:
            return user.avatar.url
        else:
            return "No image assigned to object"

    class Meta:
        model = User
        fields = (
            'id',
            'nickname',
            'email',
            'avatar_url',
            'gender',
            'birthdate',
            'about'
        )


class UserMeUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    gender = serializers.CharField(required=False)
    birthdate = serializers.DateField(required=False)
    about = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('avatar', 'gender', 'birthdate', 'about')


class UserFavouritesAddOrRemoveSerializer(serializers.Serializer):
    anime_id = serializers.IntegerField()
