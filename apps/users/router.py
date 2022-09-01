from .views import UserViewSet, UserFavoritesView

user_get_or_update = UserViewSet.as_view(
    {
        'get': 'retrieve',
        'patch': 'partial_update',
    }
)


user_favorites_router = UserFavoritesView.as_view(
    {
        'post': 'add_or_remove',
        'get': 'list',
    }
)

