from django.urls import path, include
from .views import PostViewSet
from rest_framework import routers

app_name = 'posts'
router = routers.SimpleRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]