from apps.anime.models import MyAnimeList
from django_filters.constants import EMPTY_VALUES
from django_filters import rest_framework as filters


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


class MyAnimeListFilter(filters.FilterSet):
    class Meta:
        model = MyAnimeList
        fields = ("status",)

    status = filters.CharFilter(
        help_text=(
            "Filters returned my anime list by these statutes. "
            "To return all anime do not specify this field. "
            "Valid values:"
            "```Watching```, ```Plan to watch```, "
            "```Completed```, ```Dropped```"
        ),
    )
