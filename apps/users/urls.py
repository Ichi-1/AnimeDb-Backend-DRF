from django.urls import path
from .views import UserViewSet
from djoser.views import UserViewSet as DjoserViewSet

app_name = 'users'

urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', UserViewSet.as_view({'patch': 'partial_update', 'get': 'retrieve'})),

    path('reset-password/', DjoserViewSet.as_view({'post': 'reset_password'})),
    path('reset-password-confirm/<str:uid>/<str:token>/', DjoserViewSet.as_view({'post': 'reset_password_confirm'})),
    path('set-password/', DjoserViewSet.as_view({'post': 'set_password'})),
    path('set-nickname/', DjoserViewSet.as_view({'post': 'set_username'})),

]
