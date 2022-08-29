from .views import AnimeViewSet, AlgoliaIndexAPIView, AnimeCommentViewSet
from django.urls import path
from rest_framework import routers


app_name = 'anime_db'

router = routers.SimpleRouter()
router.register(r'anime', AnimeViewSet, basename='anime')


urlpatterns = [
    path('anime/index/', AlgoliaIndexAPIView.as_view()),
    path('anime/<int:id>/comments/', AnimeCommentViewSet.as_view(
        {
            'get': 'list', 
            'post': 'create',
            # 'patch': 'partial_update',
            # 'delete': 'destroy',
        }
    )),
]
urlpatterns += router.urls




