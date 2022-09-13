
from .views import CommentView, ReviewView, ReviewCommentListView


comment_create = CommentView.as_view(
    {
        "post": "create",
    }
)

comment_update_or_delete = CommentView.as_view(
    {
        "patch": "partial_update",
        "delete": "destroy",
    }
)

review_create = ReviewView.as_view(
    {
        "post": "create",
    }
)

review_update_or_delete = ReviewView.as_view(
    {
        "patch": "partial_update",
        "delete": "destroy",
    }
)

review_comment_list = ReviewCommentListView.as_view(
    {
        "get": "list"
    }
)
