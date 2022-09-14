
from .views import CommentView, ReviewView, ReviewCommentsListView


create_comment = CommentView.as_view({
    "post": "create",
})

patch_or_delete_comment = CommentView.as_view({
    "patch": "partial_update",
    "delete": "destroy",
})

create_review = ReviewView.as_view({
    "post": "create",
})

patch_or_delete_review = ReviewView.as_view({
    "patch": "partial_update",
    "delete": "destroy"
})

get_review_comments_list = ReviewCommentsListView.as_view({
    "get": "list"
})
