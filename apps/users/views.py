from apps.anime_db.models import Anime
from apps.manga_db.models import Manga
from apps.authentication.models import User
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiExample
from .serializers import (
    UserListSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
    UserFavoritesSchema,
    FavoritesAnimeSchema,
    FavoritesMangaSchema

)
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes
from typing import List

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



class UserFavoritesView(GenericAPIView):
    http_method_names: List[str] = ["get"]
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"

    def get_serializer_class(self):
        return UserFavoritesSchema

    @extend_schema(summary="Get user favorites lists")
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = User.objects.only("id").get(id=user_id)
        favorites_anime = user.favorites_anime.only("id", "title", "poster_image").all()
        favorites_manga = user.favorites_manga.only("id", "title", "picture_main").all()

        serializer_manga = FavoritesMangaSchema(favorites_manga, many=True)
        serializer_anime = FavoritesAnimeSchema(favorites_anime, many=True)
        
        
        return Response({
                "favorites_anime": serializer_anime.data, 
                "favorites_manga": serializer_manga.data
            },
            status=status.HTTP_418_IM_A_TEAPOT
        )
