from rest_framework.routers import SimpleRouter
from .views import MangaViewSet, MangaCommentsViewSet

manga_list_or_detail = SimpleRouter()
manga_list_or_detail.register(r'manga', MangaViewSet, basename="manga")

manga_comments_list = MangaCommentsViewSet.as_view(
    {
        "get": "list",
    }
)
