from django.urls import path
from .views import AlgoliaIndexAPIView
from .router import (
    anime_list_or_detail,
    comments_update_or_delete,
    comments_list_or_create,
    reviews_list_or_create,
    reviews_detail_or_update_or_delete,
)


app_name = 'anime_db'

#   TODO В router выносятся вью содержащие более 1го метода в роуте

urlpatterns = [
    path('anime/index/', AlgoliaIndexAPIView.as_view()),
    path('anime/<int:id>/comments/', comments_list_or_create),
    path('anime/<int:id>/comments/<int:comment_id>', comments_update_or_delete),
    path('anime/<int:id>/reviews', reviews_list_or_create),
    path('anime/<int:id>/reviews/<int:review_id>', reviews_detail_or_update_or_delete)
]
urlpatterns += anime_list_or_detail.urls
