from django.urls import path
from .router import (
    manga_list,
    manga_detail,
    manga_comments_list,
    manga_review_list
)

app_name = "manga_db"

#   TODO роутинг ModelViewSet выносится в отдельный router.py

urlpatterns = [
    path("manga/", manga_list),
    path("manga/<int:id>/", manga_detail),
    path("manga/<int:id>/comments/", manga_comments_list),
    path("manga/<int:id>/reviews/", manga_review_list),
]

