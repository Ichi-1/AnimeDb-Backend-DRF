from rest_framework.serializers import ModelSerializer
from ..models import Anime


class AnimeListSerializer(ModelSerializer):
    
    class Meta:
        model = Anime
        fields = (
            'id',
            'title_en',
            'title_ja_jp',
            'poster_image',
            'studio',
            # 'description',
            'age_rating',
            'age_rating_guide',
            'average_rating',
            'episode_count',
            'episode_length',
            'release_end_year',
            'release_season',
            'release_start_year',
            'show_type',
            'tags',
        )


# class AnimeDetailsSerializer(ModelSerializer):

#     class Meta:
#         model = Anime
#         fields = ()