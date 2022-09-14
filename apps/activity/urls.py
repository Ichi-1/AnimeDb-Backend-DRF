from django.urls import path
from .router import (
    create_comment,
    create_review,
    patch_or_delete_comment,
    patch_or_delete_review,
    get_review_comments_list,
)


#   TODO роутинг ModelViewSet выносится в отдельный router.py

urlpatterns = [
    path("comments/", create_comment),
    path("reviews/", create_review),
    path("comments/<int:id>/", patch_or_delete_comment),
    path("reviews/<int:id>/", patch_or_delete_review),
    path("reviews/<int:id>/comments/", get_review_comments_list)
]
