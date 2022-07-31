from django.urls import path, include
from  .views import AnimeViewSet
from rest_framework import routers


app_name = 'anime'

router = routers.SimpleRouter()
router.register(r'animes', AnimeViewSet, basename='animes')

urlpatterns = router.urls
