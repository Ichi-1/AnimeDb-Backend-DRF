from django.urls import path
from .router import (
    get_manga_list,
    get_manga_detail,
    get_manga_comments_list,
    get_manga_reviews_list,
)
from .views import MangaFavoritesView


#   TODO роутинг ModelViewSet выносится в отдельный router.py

urlpatterns = [
    path("manga/", get_manga_list),
    path("manga/<int:id>/", get_manga_detail),
    path("manga/<int:id>/comments/", get_manga_comments_list),
    path("manga/<int:id>/reviews/", get_manga_reviews_list),
    path("manga/<int:id>/favorites/", MangaFavoritesView.as_view()),
]
