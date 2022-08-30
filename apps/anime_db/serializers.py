from rest_framework.serializers import ModelSerializer
from .models import Anime


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


class AnimeSerializer(ModelSerializer):

    class Meta:
        model = Anime
        exclude = ('staff', 'voice_actors')


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
