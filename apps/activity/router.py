from .views import CommentViewSet

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
