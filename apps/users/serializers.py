from rest_framework import serializers as s
from apps.anime_db.models import MyAnimeList
from apps.users.models import User
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from apps.anime_db.serializers import (
    AnimeStatusCountSerializer, 
    AnimeInMyListSerializer,
)
from apps.manga_db.serializers import MangaStatusCountSerializer
from apps.activity.serializers import ActivityCountSerializer


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


class MediaEntitySerializer(s.Serializer):
    id           = s.IntegerField()
    title        = s.CharField()
    poster_image = s.URLField()


class UserFavoritesSerializer(s.Serializer):
    anime = MediaEntitySerializer(many=True)
    manga = MediaEntitySerializer(many=True)


class UserStatisticSerializer(s.Serializer):
    activity = ActivityCountSerializer()
    manga    = MangaStatusCountSerializer()
    anime    = AnimeStatusCountSerializer()


class UserListStatusSerializer(s.ModelSerializer):
    class Meta:
        model = MyAnimeList
        fields = ("score", "num_episodes_watched", "updated_at")


class ListNodeSerializer(s.Serializer):
    title = s.CharField()
    poster_image = s.URLField()
    episode_count = s.IntegerField()
    list_status = s.CharField()
    my_score = s.IntegerField()
    my_num_episodes_watched = s.IntegerField()
    updated = s.DateTimeField()

