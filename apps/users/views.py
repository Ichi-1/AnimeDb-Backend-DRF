from apps.authentication.models import User
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema
from .serializers import (
    UserListSerializer,
    UserDetailSerializer,
    UserUpdateSerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes


@extend_schema_view(
    list=extend_schema(summary='Get users list'),
    retrieve=extend_schema(summary='Get user public profile'),
    partial_update=extend_schema(summary='Patch user profile. Authorized Only')
)
class UserViewSet(ModelViewSet):
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


# class UserFavoritesView(ModelViewSet):
#     queryset = User
#     serializer_class = FavoritesSerializer
#     lookup_field = 'id'
#     pagination_class = TotalCountHeaderPagination
#     # permission_cls = {
#     #     'add': [permissions.IsAuthenticated],
#     #     'remove': [permissions.IsAuthenticated],
#     #     # 'list': [permissions.AllowAny],
#     # }

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user_id = kwargs.get('id')
#         favorites_type = serializer.data['favorites_type']
#         user = get_object_or_404(User, id=user_id)
#         print(user.favourites_anime.all())

        # ? Может использовать match case ?

    # def get_permissions(self):
    #     try:
    #         return [
    #             permission() for permission in self.permission_cls[self.action]
    #         ]
    #     except KeyError:
    #         return [
    #             permission() for permission in self.permission_classes
    #         ]

    # @action(name='add', detail=False, methods=['post'])
    # def add(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     anime = get_object_or_404(Anime, id=serializer.data['anime_id'])
    #     user_favourites = anime.user_favourites.filter(id=request.user.id)

    #     if user_favourites.exists():
    #         return Response(
    #             {'detail': 'Already added to favourites. Use DELETE method to remove'},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     else:
    #         anime.user_favourites.add(request.user)
    #         return Response(
    #             {'success': 'Anime was added to favourites'},
    #             status=status.HTTP_200_OK
    #         )

    # @action(name='remove', detail=False, methods=['delete'])
    # def remove(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     anime = get_object_or_404(Anime, id=serializer.data['anime_id'])
    #     user_favourites = anime.user_favourites.filter(id=request.user.id)

    #     if user_favourites.exists():
    #         anime.user_favourites.remove(request.user)
    #         return Response(
    #             {'detail': 'Anime was removed from favourites'},
    #             status=status.HTTP_200_OK
    #         )
    #     else:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    # def list(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
