from rest_framework import serializers as s
from .models import Manga, MangaReview, MyMangaList
from apps.activity.serializers import (
    AuthorSerializer,
    ActivityCountSerializer,
    MyListSerializer, 
)
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
            'poster_image',
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
    num_chapters_readed = s.IntegerField(default=0, validators=[MaxInt(7764)])

    def validate_num_chapters_readed(self, num_chapters_readed):
        manga = Manga.objects.get(id=self.context.get("manga_id"))

        if num_chapters_readed > manga.chapters:
            raise s.ValidationError(
                {"detail": f"{manga.title} contain only {manga.chapters} chapters"}
            )
        return num_chapters_readed

    
class MangaStatusCountSerializer(s.Serializer):
    reading       = s.IntegerField(default=15)
    plan_to_read  = s.IntegerField(default=3)
    completed     = s.IntegerField(default=1)
    dropped       = s.IntegerField(default=3)


class MangaStatisticSerializer(s.Serializer):
    activity = ActivityCountSerializer()
    my_list  = MangaStatusCountSerializer()