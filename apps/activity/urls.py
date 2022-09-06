from django.urls import path
from .router import (
    comment_create,
    comment_update_or_delete,
    review_create,
    review_update_or_delete
)

app_name = 'activity'


urlpatterns = [
    path("comments/", comment_create),
    path("comments/<int:id>", comment_update_or_delete),
    path("reviews/", review_create),
    path("reviews/<int:id>", review_update_or_delete),


    # path('reviews/anime') GET list POST
    # path('reviews/manga') GET list POST
    # path('reviews/:id) GET retrieve PUT DELETE
    # path('reviews/:id/comments) GET list POST 
    # path('reviews/:id/comments/:id) GET list POST 
]