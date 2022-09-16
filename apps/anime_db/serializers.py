from rest_framework import serializers as s
from .models import Anime, AnimeReview, MyAnimeList
from apps.activity.serializers import MyListSerializer, AuthorSerializer

from django.core.validators import (
    MaxValueValidator as MaxInt,
    MinValueValidator as MinInt,
)
from faker import Faker


class AnimeDetailSerializer(s.ModelSerializer):
    class Meta:
        model = Anime
        exclude = ('staff', 'voice_actors')

    id               = s.IntegerField(default=1)
    title            = s.CharField(default="Cowboy Bebop")
    episode_count    = s.IntegerField(default=24)
    episode_length   = s.IntegerField(default=24)
    year             = s.IntegerField(default=1998)
    year_end         = s.IntegerField(default=2000)
    season           = s.CharField(default="Winter")
    age_rating       = s.CharField(default="R+")
    age_rating_guide = s.CharField(default="Violence, Profanity")
    average_rating   = s.DecimalField(default=84.91, max_digits=4, decimal_places=2)
    kind             = s.CharField(default="TV")
    description      = s.CharField(default=Faker().text())
    total_length     = s.IntegerField(validators=[MaxInt(36775)])


class AnimeListSerializer(s.ModelSerializer):
    class Meta:
        model = Anime
        fields = (
            'id',
            'title',
            'poster_image',
            'kind',
            'average_rating',
            'year',
            'tags',
        )
    id    = s.IntegerField(default=1)
    title = s.CharField(default="Cowboy Bebop")


class AnimeIndexSerializer(s.ModelSerializer):
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


class AnimeReviewListSerializer(s.ModelSerializer):
    class Meta:
        model = AnimeReview
        exclude = ("polymorphic_ctype", )

    author = AuthorSerializer()


class MyAnimeListSerializer(MyListSerializer):
    status = s.ChoiceField(choices=MyAnimeList.ListStatus.choices, default="Plan to watch")
    num_episodes_watched = s.IntegerField(default=0, validators=[MaxInt(1818), MinInt(0)])

    def validate_num_episodes_watched(self, num_episode_watched):
        """
        Check if the number of episode passed by request
        is appropriate to anime instance
        """
        anime = Anime.objects.get(id=self.context.get("anime_id"))

        if num_episode_watched  > anime.episode_count:
            raise s.ValidationError(
                {"detail": f"{anime.title} contain only {anime.episode_count} episodes"}
            )
        return num_episode_watched


class MyAnimeListResponseSerializer(s.ModelSerializer):
    class Meta:
        model  = MyAnimeList
        exclude = ("user", )
