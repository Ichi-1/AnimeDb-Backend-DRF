from django.urls import path
from .router import (
    comment_create,
    comment_update_or_delete,
    review_create,
    review_update_or_delete,
    review_comment_list
)


#   TODO роутинг ModelViewSet выносится в отдельный router.py

urlpatterns = [
    path("comments/", comment_create),
    path("comments/<int:id>/", comment_update_or_delete),
    path("reviews/", review_create),
    path("reviews/<int:id>/", review_update_or_delete),
    path("reviews/<int:id>/comments/", review_comment_list)
]
