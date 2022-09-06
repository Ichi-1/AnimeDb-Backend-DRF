from .views import CommentViewSet, ReviewViewSet

comment_create = CommentViewSet.as_view(
    {   
        "post": "create",
    }
)

comment_update_or_delete = CommentViewSet.as_view(
    {   
        "patch": "partial_update",
        "delete": "destroy",
    }
)


review_create = ReviewViewSet.as_view(
    {
        "post": "create",
    }
)

review_update_or_delete = ReviewViewSet.as_view(
    {
        "patch": "partial_update",
        "delete": "destroy",
    }
)