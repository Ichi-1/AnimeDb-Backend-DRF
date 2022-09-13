from .views import AnimeView, AnimeCommentsView, AnimeReviewView


anime_list = AnimeView.as_view(
    {
        "get": "list"
    }
)

anime_detail = AnimeView.as_view(
    {
        "get": "retrieve"
    }
)

anime_comments_list = AnimeCommentsView.as_view(
    {
        "get": "list"
    }
)

anime_review_list = AnimeReviewView.as_view(
    {
        "get": "list"
    }
)
