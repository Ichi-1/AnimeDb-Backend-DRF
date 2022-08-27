from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from apps.anime_db.models import Anime


@register(Anime)
class AnimeIndex(AlgoliaIndex):
    # by default - model pk
    # custom_objectID = 'title'
    fields = [
        'title',
        'poster_image',
        'kind',
        'average_rating',
        'studio',
        'year',
        'episode_count',
    ]

    settings = {
        'customRanking': [
            'desc(average_rating)'
        ],
        'ranking': [
            'desc(average_rating)',
            'desc(year)',
            'asc(year)',
        ],
        'searchableAttributes': [
            'title',
            'studio',
            'year',
            'kind',
        ],
        'attributesForFaceting': [
            'studio',
            'kind',
            'year',
            'episode_count',
        ],

    }

    tags = 'get_tags_list'
