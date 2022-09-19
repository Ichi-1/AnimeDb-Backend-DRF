from django.urls import path
from djoser.views import UserViewSet as Djoser
from .views import (
    UserView, 
    UserFavoritesView, 
    UserMyAnimeListView,
    UserStatisticView
)
from .router import (
    get_or_patch_user,
)

app_name = "users"

#   TODO роутинг ModelViewSet выносится в отдельный router.py

urlpatterns = [
    path("users/", UserView.as_view({"get": "list"})),
    path("users/<int:pk>/", get_or_patch_user),
    path("users/<int:id>/list/anime/", UserMyAnimeListView.as_view()),
    path("users/<int:id>/statistic/", UserStatisticView.as_view()),
    path("users/<int:id>/favorites/", UserFavoritesView.as_view()),
    # user auth-kinda endpoints
    path("users/reset-password/", Djoser.as_view({"post": "reset_password"})),
    path("users/reset-password-confirm/<str:uid>/<str:token>/", Djoser.as_view({"post": "reset_password_confirm"})),
    path("users/set-password/", Djoser.as_view({"post": "set_password"})),
    path("users/set-nickname/", Djoser.as_view({"post": "set_username"})),
]
