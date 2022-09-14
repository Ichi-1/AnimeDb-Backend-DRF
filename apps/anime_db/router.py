from .views import (
    AnimeView,
    AnimeCommentsView,
    AnimeReviewView,
)


get_anime_list = AnimeView.as_view({
    "get": "list"
})

get_anime_detail = AnimeView.as_view({
    "get": "retrieve"
})

get_anime_comments_list = AnimeCommentsView.as_view({
    "get": "list"
})

get_anime_reviews_list = AnimeReviewView.as_view({
    "get": "list"
})
