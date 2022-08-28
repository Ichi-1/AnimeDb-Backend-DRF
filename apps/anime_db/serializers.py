from rest_framework.serializers import ModelSerializer

from apps.activity.models import Comment
from .models import Anime



class AnimeCommentsSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            'user_id', 
            'commentable_id',
            'body', 
            'created_at', 
            'updated_at'
        )


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
    # comments = AnimeCommentsSerializer(many=True)

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
