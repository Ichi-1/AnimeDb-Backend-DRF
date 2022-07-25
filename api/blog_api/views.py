
from rest_framework.generics import (
    ListCreateAPIView, 
    RetrieveDestroyAPIView
)
from apps.blog.models import Post
from .serializers import PostSerializer


class PostList(ListCreateAPIView):
    queryset = Post.custom_objects.all()
    serializer_class = PostSerializer

class PostDetail(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer