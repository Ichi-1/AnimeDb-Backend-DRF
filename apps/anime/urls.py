from django.urls import path
from .views import AnimeFavoritesView, MyAnimeListView, AnimeStatisticView
from .router import (
    get_anime_list,
    get_anime_detail,
    get_anime_comments_list,
    get_anime_reviews_list,
    get_list_or_create_screenshot,
)

#   TODO роутинг ModelViewSet выносится в отдельный router.py

urlpatterns = [
    path('anime/', get_anime_list),
    path('anime/<int:id>/', get_anime_detail),
    path('anime/<int:id>/comments/', get_anime_comments_list),
    path('anime/<int:id>/reviews/', get_anime_reviews_list),
    path("anime/<int:id>/favorites/", AnimeFavoritesView.as_view()),
    path("anime/<int:id>/my_list/", MyAnimeListView.as_view()),
    path("anime/<int:id>/statistic/", AnimeStatisticView.as_view()),
    path("anime/<int:id>/screenshot/", get_list_or_create_screenshot)
]
