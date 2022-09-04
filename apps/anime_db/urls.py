from django.urls import path
from .views import AlgoliaIndexAPIView
from .router import (
    anime_list_or_detail,
    anime_comments_list,
)


app_name = 'anime_db'

#   TODO В router выносятся вью содержащие более 1го метода в роуте

urlpatterns = [
    path('anime/index/', AlgoliaIndexAPIView.as_view()),
    path('anime/<int:id>/comments/', anime_comments_list),
    # path('anime/<int:id>/reviews', reviews_list_or_create),
]
urlpatterns += anime_list_or_detail.urls
