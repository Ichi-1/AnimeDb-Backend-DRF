from .views import AnimeViewSet, AlgoliaIndexAPIView
from django.urls import path
from rest_framework import routers


app_name = 'animes'

router = routers.SimpleRouter()
router.register(r'animes', AnimeViewSet, basename='animes')


urlpatterns = [
    path('animes/index/', AlgoliaIndexAPIView.as_view()),
    # path('animes/comments/', CommentViewSet.as_view()),
]
urlpatterns += router.urls




