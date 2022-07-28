from django.urls import path, include
from  .views import AnimeViewSet
from rest_framework import routers


app_name = 'anime-api'

router = routers.SimpleRouter()
router.register(r'animes', AnimeViewSet)
print(router.urls)

urlpatterns = router.urls
