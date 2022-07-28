from apps.blog.models import Post
from rest_framework.generics import (
    ListCreateAPIView, 
    ListAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView, 
)
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import (
    BasePermission,
    IsAdminUser, 
    IsAuthenticatedOrReadOnly,
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


class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    
    serializer_class = PostSerializer
    queryset  = Post.objects.all()
    permission_classes = [PostUserWritePermission]
