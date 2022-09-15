from .views import (
    AnimeView,
    AnimeCommentsListView,
    AnimeReviewsListView,
)


get_anime_list = AnimeView.as_view({
    "get": "list"
})

get_anime_detail = AnimeView.as_view({
    "get": "retrieve"
})

get_anime_comments_list = AnimeCommentsListView.as_view({
    "get": "list"
})

get_anime_reviews_list = AnimeReviewsListView.as_view({
    "get": "list"
})
