from rest_framework import routers
from .views import AnimeViewSet, AnimeCommentViewSet, AnimeReviewViewSet


anime_list_or_detail = routers.SimpleRouter()
anime_list_or_detail.register(r'anime', AnimeViewSet, basename='anime')


comments_list_or_create = AnimeCommentViewSet.as_view(
    {
        'get': 'list',
        'post': 'create'
    }
)

comments_update_or_delete = AnimeCommentViewSet.as_view(
    {
        'delete': 'destroy',
        'patch': 'partial_update',
    }
)

reviews_list_or_create = AnimeReviewViewSet.as_view(
    {
        'get': 'list',
        'post': 'create',
    }
)

reviews_detail_or_update_or_delete = AnimeCommentViewSet.as_view(
    {
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy',
    }
)