from django.urls import path
from .views import AlgoliaIndexAPIView
from .router import (
    anime_list_or_detail,
    comments_delete_or_update,
    comments_list_or_create
)


app_name = 'anime_db'

#   TODO В router выносятся вью содержащие более 1го метода в роуте

urlpatterns = [
    path('anime/index/', AlgoliaIndexAPIView.as_view()),
    path('anime/<int:id>/comments/', comments_list_or_create),
    path('anime/<int:id>/comments/<int:comment_id>', comments_delete_or_update)
]
urlpatterns += anime_list_or_detail.urls
