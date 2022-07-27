from django.urls import path
from  .views import AnimeDetail, AnimeList


app_name = 'anime-api'

urlpatterns = [
    path('api/animes', AnimeList.as_view(), name='anime-list'),
    path('api/animes/<int:pk>/', AnimeDetail.as_view(), name='anime-detail'),
]
