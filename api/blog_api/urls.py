from django.urls import path
from .views import (
    PostList, PostDetail
)


app_name = 'blog-api'

urlpatterns = [
    path('api/posts/', PostList.as_view(), name='post-list'),
    path('api/posts/<int:pk>/', PostDetail.as_view(), name='post-detail'), 
]