from .views import AnimeViewSet, AlgoliaIndexAPIView, AnimeCommentViewSet
from django.urls import path
from rest_framework import routers


app_name = 'anime_db'

#   TODO В отдельный api_router выносятся вью содержащие более 1го метода в 1 роуте

anime_list_or_detail = routers.SimpleRouter()
anime_list_or_detail.register(r'anime', AnimeViewSet, basename='anime')

comments_list_or_create = AnimeCommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }
)

comments_delete_or_update = AnimeCommentViewSet.as_view({
        'delete': 'destroy',
        'patch': 'partial_update',
    }
)


urlpatterns = [
    path('anime/index/', AlgoliaIndexAPIView.as_view()),
    path('anime/<int:id>/comments/', comments_list_or_create),
    path('anime/<int:id>/comments/<int:comment_id>', comments_delete_or_update)
]
urlpatterns += anime_list_or_detail.urls
