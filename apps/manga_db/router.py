from .views import (
    MangaView,
    MangaCommentsView,
    MangaReviewsView
)

get_manga_list = MangaView.as_view({
    "get": "list"
})

get_manga_detail = MangaView.as_view({
    "get": "retrieve"
})

get_manga_comments_list = MangaCommentsView.as_view({
    "get": "list"
})

get_manga_reviews_list = MangaReviewsView.as_view({
    "get": "list"
})
