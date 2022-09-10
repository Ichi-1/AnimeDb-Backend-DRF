from django.urls import path
from djoser.views import UserViewSet as Djoser
from .views import UserViewSet
from .router import user_get_or_update
# user_favorites_router

app_name = 'users'

#   TODO роутинг ModelViewSet выносится в отдельный router.py

urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', user_get_or_update),
    # path('<int:pk>/favorites/', user_favorites_router),
    path('reset-password/', Djoser.as_view({'post': 'reset_password'})),
    path('reset-password-confirm/<str:uid>/<str:token>/', Djoser.as_view({'post': 'reset_password_confirm'})),
    path('set-password/', Djoser.as_view({'post': 'set_password'})),
    path('set-nickname/', Djoser.as_view({'post': 'set_username'})),
]
