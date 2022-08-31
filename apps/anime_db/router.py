from rest_framework import routers
from .views import AnimeViewSet, AnimeCommentViewSet


anime_list_or_detail = routers.SimpleRouter()
anime_list_or_detail.register(r'anime', AnimeViewSet, basename='anime')


comments_list_or_create = AnimeCommentViewSet.as_view(
    {
        'get': 'list',
        'post': 'create'
    }
)

comments_delete_or_update = AnimeCommentViewSet.as_view(
    {
        'delete': 'destroy',
        'patch': 'partial_update',
    }
)
