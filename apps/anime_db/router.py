from rest_framework import routers
from .views import AnimeViewSet, AnimeCommentsViewSet


anime_list_or_detail = routers.SimpleRouter()
anime_list_or_detail.register(r'anime', AnimeViewSet, basename='anime')


anime_comments_list = AnimeCommentsViewSet.as_view(
    {
        'get': 'list',
    }
)
