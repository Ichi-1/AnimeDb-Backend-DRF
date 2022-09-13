from rest_framework.serializers import ModelSerializer
from .models import Manga


class MangaDetailSerializer(ModelSerializer):
    class Meta:
        model = Manga
        fields = '__all__'


class MangaListSerializer(ModelSerializer):
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
