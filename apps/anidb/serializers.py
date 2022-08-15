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


class AnimeDetailsSerializer(ModelSerializer):

    class Meta:
        model = Anime
        fields = (
            'id',
            'title',
            'title_jp',
            'poster_image',
            'studio',
            'description',
            'age_rating',
            'age_rating_guide',
            'average_rating',
            'episode_count',
            'episode_length',
            'year',
            'year_end',
            'season',
            'kind',
            'tags',
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