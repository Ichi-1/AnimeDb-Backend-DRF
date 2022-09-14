from django.urls import path
from .views import AnimeFavoritesView
from .router import (
    get_anime_list,
    get_anime_detail,
    get_anime_comments_list,
    get_anime_reviews_list,
)

#   TODO роутинг ModelViewSet выносится в отдельный router.py

urlpatterns = [
    path('anime/', get_anime_list),
    path('anime/<int:id>/', get_anime_detail),
    path('anime/<int:id>/comments/', get_anime_comments_list),
    path('anime/<int:id>/reviews/', get_anime_reviews_list),
    path("anime/<int:id>/favorites/", AnimeFavoritesView.as_view())
    # path('anime/index/', AlgoliaIndexAPIView.as_view()),
]
