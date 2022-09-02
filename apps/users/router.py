from .views import UserViewSet, UserFavoritesView

user_get_or_update = UserViewSet.as_view(
    {
        'get': 'retrieve',
        'patch': 'partial_update',
    }
)


user_favorites_router = UserFavoritesView.as_view(
    {
        'post': 'create',
        'get': 'list',
    }
)

