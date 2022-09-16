from rest_framework import serializers as s
from .models import Manga, MangaReview, MyMangaList
from apps.activity.serializers import MyListSerializer, AuthorSerializer
from django.core.validators import MaxValueValidator as MaxInt


class MangaDetailSerializer(s.ModelSerializer):
    class Meta:
        model = Manga
        fields = '__all__'


class MangaListSerializer(s.ModelSerializer):
    class Meta:
        model = Manga
        fields = (
            'id',
            'title',
            'media_type',
            'picture_main',
            'year_start',
            'tags',
        )


class MangaReviewListSerializer(s.ModelSerializer):
    class Meta:
        model = MangaReview
        exclude = ("polymorphic_ctype", )

    author = AuthorSerializer()


class MyMangaListSerializer(MyListSerializer):
    status = s.ChoiceField(choices=MyMangaList.ListStatus.choices, default="Plan to read")
    num_chapters_read = s.IntegerField(default=0, validators=[MaxInt(7764)])
