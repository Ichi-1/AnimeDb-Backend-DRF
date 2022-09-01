from rest_framework.serializers import ModelSerializer, Serializer, IntegerField
from .models import Anime


class AnimeDetailSerializer(ModelSerializer):

    class Meta:
        model = Anime
        exclude = ('staff', 'voice_actors')


class AnimeListSerializer(ModelSerializer):

    class Meta:
        model = Anime
        fields = (
            'id',
            'title',
            'poster_image',
            'kind',
            'year',
            'tags',
            'average_rating',
            'path',
        )


class AnimeIndexSerializer(ModelSerializer):

    class Meta:
        model = Anime
        fields = (
            'id',
            'title',
            'poster_image',
            'kind',
            'average_rating',
            'studio',
            'year',
            'episode_count',
        )
