from rest_framework import serializers
from .models import Anime


class AnimeListSerializer(serializers.ModelSerializer):

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


class AnimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Anime
        exclude = ('staff', 'voice_actors')


class AnimeIndexSerializer(serializers.ModelSerializer):

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
