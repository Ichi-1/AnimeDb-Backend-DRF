from apps.blog.models import Post
from rest_framework.generics import (
    ListCreateAPIView, 
    ListAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import (
    BasePermission,
    IsAdminUser, 
    DjangoModelPermissionsOrAnonReadOnly,
    SAFE_METHODS,
)
from .api.serializers import PostSerializer


class PostUserWritePermission(BasePermission):
    message = 'Editing post is restricted to the author only'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class PostList(ListAPIView):
    queryset = Post.custom_objects.all()
    serializer_class = PostSerializer

class PostDetail(RetrieveDestroyAPIView):
    permission_classes = [PostUserWritePermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer