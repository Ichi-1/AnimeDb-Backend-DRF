from rest_framework import serializers as s
from apps.users.models import User
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from apps.anime_db.models import Anime
from apps.manga_db.models import Manga


class UserListSerializer(s.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'nickname',
            'avatar_url',
            'last_login',
            'created_at',
        )

    avatar_url = s.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.URI)
    def get_avatar_url(self, user: dict) -> str:
        if user.avatar:
            return user.avatar.url
        else:
            return "No image assigned to object"


class UserDetailSerializer(s.ModelSerializer):
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

    avatar_url = s.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.URI)
    def get_avatar_url(self, user: dict) -> str:
        if user.avatar:
            return user.avatar.url
        else:
            return "No image assigned to object"


class UserUpdateSerializer(s.Serializer):
    avatar    = s.ImageField(required=False)
    gender    = s.CharField(required=False)
    birthdate = s.DateField(required=False)
    about     = s.CharField(required=False)


class FavoritesAnimeSerializer(s.ModelSerializer):
    class Meta:
        model = Anime
        fields = ("id", "title", "poster_image")


class FavoritesMangaSerializer(s.ModelSerializer):
    class Meta:
        model = Manga
        fields = ("id", "title", "picture_main")


class UserFavoritesSerializer(s.Serializer):
    favorites_anime = FavoritesAnimeSerializer(many=True)
    favorites_manga = FavoritesMangaSerializer(many=True)
