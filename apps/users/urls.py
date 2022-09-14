from django.urls import path
from djoser.views import UserViewSet as Djoser
from .views import UserView
from .router import (
    get_or_patch_user,
)

app_name = 'users'

#   TODO роутинг ModelViewSet выносится в отдельный router.py

urlpatterns = [
    # user recources
    path('users/', UserView.as_view({'get': 'list'})),
    path('users/<int:pk>/', get_or_patch_user),
    # path('users/<int:pk>/comments/', get_user_comments_list),
    # path('users/<int:pk>/reviews/', get_user_reviews_list),
    # path('users/<int:pk>/favorites/', get_user_favorites_list),
    # path('<int:pk>/favorites/', user_favorites_router),
    path('users/reset-password/', Djoser.as_view({'post': 'reset_password'})),
    path('users/reset-password-confirm/<str:uid>/<str:token>/', Djoser.as_view({'post': 'reset_password_confirm'})),
    path('users/set-password/', Djoser.as_view({'post': 'set_password'})),
    path('users/set-nickname/', Djoser.as_view({'post': 'set_username'})),
]
