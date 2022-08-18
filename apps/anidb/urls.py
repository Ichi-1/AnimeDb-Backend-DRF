from .views import AnimeViewSet, IndexAPIView
from django.urls import path
from rest_framework import routers


app_name = 'animes'

router = routers.SimpleRouter()
router.register(r'animes', AnimeViewSet, basename='animes')


urlpatterns = [
    path('animes/index/', IndexAPIView.as_view()),
]
urlpatterns += router.urls




