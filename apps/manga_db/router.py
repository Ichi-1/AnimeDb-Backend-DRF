from .views import MangaView, MangaCommentsView, MangaReviewsView

manga_list = MangaView.as_view(
    {
        "get": "list"
    }
)

manga_detail = MangaView.as_view(
    {
        "get": "retrieve"
    }
)

manga_comments_list = MangaCommentsView.as_view(
    {
        "get": "list",
    }
)

manga_review_list = MangaReviewsView.as_view(
    {
        "get": "list"
    }
)
