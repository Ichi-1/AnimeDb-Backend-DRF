from django.urls import path
from .views import UserViewSet
from djoser.views import UserViewSet as DjoserViewSet

app_name = 'users'

urlpatterns = [
    path('users/', UserViewSet.as_view({'get':'list'})),
    path('users/me/<int:id>/', DjoserViewSet.as_view({'get':'retrieve', 'patch':'update'})),
]