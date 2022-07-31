from apps.anidb.models import Anime
from django_filters import rest_framework as filters


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class AnimeFilter(filters.FilterSet):
    year = filters.RangeFilter()

    class Meta:
        model = Anime
        fields = ('kind', 'year')
