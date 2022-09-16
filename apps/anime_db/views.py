from apps.activity.models import Comment
from apps.users.models import User
from apps.activity.paging import CommentListPaginator
from apps.activity.serializers import CommentsListSerializer

from core.serializers import EmptySerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from .models import Anime, AnimeReview, MyAnimeList
from .utils.filterset import AnimeListFilter
from .utils.paging import TotalCountHeaderPagination
from .serializers import (
    AnimeDetailSerializer,
    AnimeListSerializer,
    AnimeReviewListSerializer,
    MyAnimeListSerializer,
    MyAnimeListResponseSerializer
)


@extend_schema_view(
    list=extend_schema(summary="Get anime list"),
    retrieve=extend_schema(summary="Get anime details")
)
class AnimeView(ModelViewSet):
    queryset = Anime.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filterset_class = AnimeListFilter
    search_fields = ["title", "^title", "year"]
    ordering_fields = ["title", "year", "?"]
    pagination_class = TotalCountHeaderPagination
    ordering = ["-average_rating"]  # default ordering
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action == "list":
            return AnimeListSerializer
        if self.action == "retrieve":
            return AnimeDetailSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Get anime comments list",
        description=(
            "If commentable resource has no comments, "
            "return empty list ```200 Ok```"
        )
    )
)
class AnimeCommentsListView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CommentListPaginator
    lookup_field = "id"

    def list(self, request, *args, **kwargs):
        commentable_anime = get_object_or_404(Anime, id=kwargs.get("id"))
        comments = commentable_anime.comments.all().order_by("created_at")
        page = self.paginate_queryset(comments)
        serializer = self.get_serializer(page, many=True)
        # TODO Если комментариев к ресурсу нет - возвращается пустой массив
        return self.get_paginated_response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="Get anime reviews list",
        description=(
            "If reviewable resource has no review, "
            "return empty list ```200 Ok```"
        )
    )
)
class AnimeReviewsListView(ModelViewSet):
    queryset = AnimeReview.objects.all().order_by("created_at")
    serializer_class = AnimeReviewListSerializer
    pagination_class = TotalCountHeaderPagination
    lookup_field = "anime_id"


@extend_schema_view(
    put=extend_schema(
        summary="Update my favorites anime",
        description=(
            "Add specific anime to my favorites list. "
            "If anime already added to user favorites"
            "this endpoint does nothing and returns ```409 Conflict```"
        )
    ),
    delete=extend_schema(
        summary="Delete my favorites anime",
        description=(
            "If the specified anime does not exist in user's anime list"
            "this endpoint does nothing and returns ```404 Not Found```."
        )
    )
)
class AnimeFavoritesView(GenericAPIView):
    http_method_names = ["put", "delete"]
    queryset = Anime.objects.all()
    serializer_class = EmptySerializer
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        anime_id = kwargs.get("id")
        anime = get_object_or_404(Anime, id=anime_id)
        user_favorites = anime.user_favorites.filter(id=request.user.id)

        if user_favorites.exists():
            return Response(
                {"detail": f"'{anime.title}' already added to favorites"},
                status=status.HTTP_409_CONFLICT
            )
        anime.user_favorites.add(request.user)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        anime_id = kwargs.get("id")
        anime = get_object_or_404(Anime, id=anime_id)
        user_favorites = anime.user_favorites.filter(id=request.user.id)

        if not user_favorites.exists():
            return Response(
                {"detail": f"'{anime.title}' not added to favorites"},
                status=status.HTTP_404_NOT_FOUND
            )
        anime.user_favorites.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    put=extend_schema(
        summary="Update my anime list status",
        description=(
            "Add specified anime to my anime list. "
            "If specified anime already in myanimelist, update its status. "
            "This endpoint updates only values specified by the parameter."
        ),
        responses=MyAnimeListResponseSerializer
    ),
    delete=extend_schema(
        summary="Delete my anime list item",
        description=(
            "If the specified anime does not exist in user's anime list, "
            "this endpoint does nothing and returns ```404 Not Found```."
        )
    )
)
class MyAnimeListView(GenericAPIView):
    http_method_names = ["put", "delete"]
    queryset = MyAnimeList.objects.all()
    serializer_class = MyAnimeListSerializer
    lookup_field = "id"

    def create_or_update(self, validated_data, request, anime):
        """
        If user has no relation to anime in MyAnimeList,
        new relation would be created with given validated_date.
        If relation exist, update it with new incoming data
        """
        user = User.objects.only("pk").get(pk=request.user.id)
        my_list_status = self.queryset.filter(anime=anime, user=user)
        my_list_status.update_or_create(defaults=validated_data, anime=anime, user=user)

    def get_serializer_context(self):
        """
        Adding anime_id to context object, to
        get anime instance by id for validation puprose into serializer method:

        ```
        def validate_num_episode_watched(self, num_watched_episode):
            anime = Anime.objects.get(id=self.context.get("anime_id"))
            # validation logic
        ```
        """
        context = super().get_serializer_context()
        context["anime_id"] = self.kwargs["id"]
        return context

    def put(self, request, *args, **kwargs):
        anime = get_object_or_404(Anime, id=kwargs.get("id"))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.create_or_update(serializer.data, request, anime)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        pass
