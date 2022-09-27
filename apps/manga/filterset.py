from apps.manga.models import MyMangaList
from django_filters import rest_framework as filters


class MyMangaListFilter(filters.FilterSet):
    class Meta:
        model = MyMangaList
        fields = ("status", )

    status = filters.CharFilter(
        help_text=(
            "Filters returned my manga list by these statutes. "
            "To return all manga do not specify this field. "
            "Valid values:"
            "```Reading```, ```Plan to read```, "
            "```Completed```, ```Dropped```"
        )
    )
