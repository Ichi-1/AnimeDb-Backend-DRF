from apps.authentication.models import User
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiExample
from .serializers import (
    UserListSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
    UserFavoritesSerializer,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes


@extend_schema_view(
    list=extend_schema(summary='Get users list'),
    retrieve=extend_schema(summary='Get user public profile'),
    partial_update=extend_schema(summary='Patch user profile. Authorized Only'),
)
class UserView(ModelViewSet):
    queryset = User.objects.all().order_by('-last_login')
    parser_classes = [FormParser, MultiPartParser]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        if self.action == 'partial_update':
            return UserUpdateSerializer
        if self.action == 'retrieve':
            return UserDetailSerializer

    @permission_classes([permissions.IsAuthenticated])
    def partial_update(self, request, *args, **kwargs):
        user_id = request.user.id
        user_to_update = kwargs['pk']

        if user_id != user_to_update:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, args, kwargs)


class UserFavoritesView(ModelViewSet):
    serializer_class = UserFavoritesSerializer

    @extend_schema(
        summary="Get user favorites list",
        responses=OpenApiExample(
            name="User favorites",

        )
    )
    @permission_classes([permissions.AllowAny])
    def list(self, request, *args, **kwargs):
        """
        Should return nested serializer,
        which contain favorites diveded by type -
        {
            "favorites_anime": {
                {
                    "id": 1,
                    "title": "Cowboy Bebop",
                    "poster_image": "http://example1.com",
                },
                {
                    "id": 15,
                    "title": "Death Note",
                    "poster_image": "http://example1.com",
                },
            },
            "favorites_manga": {
                {
                    "id": 4,
                    "title": "Vinland Saga",
                    "poster_image": "http://example1.com",
                },
                {
                    "id": 1,
                    "title": "Berserk",
                    "poster_image": "http://example1.com",
                },
            }
        }
        """
        pass
