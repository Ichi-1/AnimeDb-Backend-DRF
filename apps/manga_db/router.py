from .views import MangaViewSet, MangaCommentsViewSet, MangaReviewsViewSet

manga_list = MangaViewSet.as_view(
    {
        "get": "list"
    }
)

manga_detail = MangaViewSet.as_view(
    {
        "get": "retrieve"
    }
)

manga_comments_list = MangaCommentsViewSet.as_view(
    {
        "get": "list",
    }
)

manga_review_list = MangaReviewsViewSet.as_view(
    {
        "get": "list"
    }
)