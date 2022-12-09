from apps.anime.utils.filterset import MyAnimeListFilter
from apps.manga.filterset import MyMangaListFilter
from apps.users.models import User
from apps.anime.models import MyAnimeList
from apps.manga.models import MyMangaList
from apps.activity.models import Comment, Review
from django.db.models import F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema_view, extend_schema
)
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    MediaEntitySerializer,
    MyAnimeListGetSerializer,
    MyMangaListGetSerializer,
    UserListSerializer,
    UserDetailSerializer,
    UserFavoritesSerializer,
    UserStatisticSerializer,
    UserUpdateSerializer,
)


# TODO пофиксить загрузку файла в API схеме сваггера
@extend_schema_view(
    list=extend_schema(summary='Get users list'),
    retrieve=extend_schema(summary='Get user public profile'),
    partial_update=extend_schema(
        summary='Patch user profile. Authorized Only',
    ),
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
    def partial_update(self, request: Request, *args, **kwargs):
        user_id = request.user.id
        user_to_update = kwargs['pk']

        if user_id != user_to_update:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, args, kwargs)


@extend_schema_view(
    get=extend_schema(
        summary="Get user favorites",
        description=(
            "If user has no favorites "
            "would be returned json with emply lists ```200```"
        ),
    )
)
class UserFavoritesView(GenericAPIView):
    http_method_names = ["get"]
    queryset = User.objects.all()
    serializer_class = UserFavoritesSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"

    def get(self, request: Request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = User.objects.only("id").get(id=user_id)
        favorites_anime = user.favorites_anime.only("id", "title", "poster_image").all()
        favorites_manga = user.favorites_manga.only("id", "title", "poster_image").all()

        serializer_manga = MediaEntitySerializer(favorites_manga, many=True)
        serializer_anime = MediaEntitySerializer(favorites_anime, many=True)

        return Response({
            "anime": serializer_anime.data,
            "manga": serializer_manga.data
        })


@extend_schema_view(
    get=extend_schema(
        summary="Get user statistic",
        description=(
            "Retrieve count of user activity and list status "
            "count for different type of media entity. "
            "Response status always ```200```, except user not found ```404```"
        )
    )
)
class UserStatisticView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserStatisticSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs.get("id"))
        my_anime_list = MyAnimeList.objects.select_related("user").filter(user=user)
        my_manga_list = MyMangaList.objects.select_related("user").filter(user=user)
        my_comments   = Comment.objects.filter(author=user)
        my_reviews    = Review.objects.filter(author=user)

        user_statistic = {
            "activity": {
                "comments": my_comments.count(),
                "reviews": my_reviews.count(),
            },
            "anime": {
                "watching": my_anime_list.filter(status="Watching").count(),
                "plan_to_watch": my_anime_list.filter(status="Plan to watch").count(),
                "completed": my_anime_list.filter(status="Completed").count(),
                "dropped": my_anime_list.filter(status="Dropped").count()
            },
            "manga": {
                "reading": my_manga_list.filter(status="Reading").count(),
                "plan_to_read": my_manga_list.filter(status="Plan to read").count(),
                "completed": my_manga_list.filter(status="Completed").count(),
                "dropped": my_manga_list.filter(status="Dropped").count()
            }
        }
        return Response(user_statistic)


@extend_schema_view(
    get=extend_schema(
        summary="Get MyAnimeList",
        description=(
            "This endpoint always return ```200``` "
            "except user not found ```404```"
        )
    )
)
class UserMyAnimeListView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MyAnimeListGetSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = MyAnimeListFilter
    lookup_field = "id"

    def get_queryset(self):
        """
        F expression used to rename field of related(FK) anime instance.\n
        In get method we only filter this queryset against path and query params.\n
        ```users/:id/list/anime/?status=Dropped```
        """
        return MyAnimeList.objects.all().select_related("anime").values(
            title=F("anime__title"),
            poster_image=F("anime__poster_image"),
            kind=F("anime__kind"),
            episode_count=F("anime__episode_count"),
            list_status=F("status"),
            my_score=F("score"),
            updated=F("updated_at"),
            my_num_episodes_watched=F("num_episodes_watched"),
        )


@extend_schema_view(
    get=extend_schema(
        summary="Get MyMangaList",
        description=(
            "This endpoint always return ```200``` "
            "except user not found ```404```"
        )
    )
)
class UserMyMangaListView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MyMangaListGetSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = MyMangaListFilter
    lookup_field = "id"

    def get_queryset(self):
        return MyMangaList.objects.all().select_related("manga").values(
            title=F("manga__title"),
            poster_image=F("manga__poster_image"),
            media_type=F("manga__media_type"),
            chapters=F("manga__chapters"),
            list_status=F("status"),
            my_score=F("score"),
            updated=F("updated_at"),
            my_num_chapters_readed=F("num_chapters_readed")
        )
