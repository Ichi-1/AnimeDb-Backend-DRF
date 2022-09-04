from .views import UserViewSet


user_get_or_update = UserViewSet.as_view(
    {
        'get': 'retrieve',
        'patch': 'partial_update',
    }
)
