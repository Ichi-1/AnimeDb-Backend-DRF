from django.urls import path
from djoser.views import UserViewSet as Djoser
from .views import UserViewSet

app_name = 'users'

# TODO В отдельный api_router выносятся вью содержащие более 1го метода в 1 роуте

user_get_or_update = UserViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
    }
)


urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', user_get_or_update),
    path('reset-password/', Djoser.as_view({'post': 'reset_password'})),
    path('reset-password-confirm/<str:uid>/<str:token>/', Djoser.as_view({'post': 'reset_password_confirm'})),
    path('set-password/', Djoser.as_view({'post': 'set_password'})),
    path('set-nickname/', Djoser.as_view({'post': 'set_username'})),
]
