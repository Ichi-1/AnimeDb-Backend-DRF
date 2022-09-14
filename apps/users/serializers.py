from rest_framework import serializers
from apps.authentication.models import User
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from apps.anime_db.models import Anime
from apps.manga_db.models import Manga

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'nickname',
            'avatar_url',
            'last_login',
            'created_at',
        )

    avatar_url = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.URI)
    def get_avatar_url(self, user: dict) -> str:
        if user.avatar:
            return user.avatar.url
        else:
            return "No image assigned to object"


class UserDetailSerializer(serializers.ModelSerializer):
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

    avatar_url = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.URI)
    def get_avatar_url(self, user: dict) -> str:
        if user.avatar:
            return user.avatar.url
        else:
            return "No image assigned to object"


class UserUpdateSerializer(serializers.Serializer):
    avatar    = serializers.ImageField(required=False)
    gender    = serializers.CharField(required=False)
    birthdate = serializers.DateField(required=False)
    about     = serializers.CharField(required=False)


class FavoritesAnimeSchema(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ("id", "title", "poster_image")


class FavoritesMangaSchema(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = ("id", "title", "picture_main")


class UserFavoritesSchema(serializers.Serializer):
    favorites_anime = FavoritesAnimeSchema(many=True)
    favorites_manga = FavoritesMangaSchema(many=True)