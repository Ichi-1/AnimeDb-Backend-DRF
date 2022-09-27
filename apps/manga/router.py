from .views import (
    MangaView,
    MangaCommentsListView,
    MangaReviewsListView
)

get_manga_list = MangaView.as_view({
    "get": "list"
})

get_manga_detail = MangaView.as_view({
    "get": "retrieve"
})

get_manga_comments_list = MangaCommentsListView.as_view({
    "get": "list"
})

get_manga_reviews_list = MangaReviewsListView.as_view({
    "get": "list"
})
