from django.urls import path
from .router import (
    manga_list_or_detail,
    manga_comments_list,
)

app_name = "manga_db"

#   TODO роутинг ModelViewSet выносится в отдельный router.py

urlpatterns = [
    path("manga/<int:id>/comments/", manga_comments_list),
]

urlpatterns += manga_list_or_detail.urls
