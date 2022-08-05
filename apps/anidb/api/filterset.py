from apps.anidb.models import Anime
from django_filters.constants import EMPTY_VALUES
from django_filters import rest_framework as filters


#TODO Tags filter doesnt work properly

class ListFilter(filters.Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        value_list = value.split(',')
        qs = super().filter(qs, value_list)
        return qs


class AnimeListFilter(filters.FilterSet):
    kind = ListFilter(field_name='kind', lookup_expr='in')
    year = filters.RangeFilter(field_name='year')
    tags = filters.CharFilter(field_name='tags', lookup_expr='icontains')
