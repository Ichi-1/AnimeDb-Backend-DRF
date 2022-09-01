from apps.activity.models import Comment, Review
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import mixins, generics, permissions, viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from .models import Anime
from .utils.algolia import perform_serach
from .utils.filterset import AnimeListFilter
from .utils.paginator import TotalCountHeaderPagination
from .serializers import (
    AnimeDetailSerializer,
    AnimeIndexSerializer,
    AnimeListSerializer,
)
from apps.activity.serializers import (
    CommentCreateSerializer,
    CommentUpdateSerializer,
    CommentsListSerializer,
    ReviewListSerializer
)


class AnimeViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    GET /anime/ - retrieve list of all anime contained in database;
    GET /anime/:id - retrieve instance of anime by id;
    """
    queryset = Anime.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filterset_class = AnimeListFilter
    search_fields = ['title', '^title', 'year']
    ordering_fields = ['title', 'year', '?']
    pagination_class = TotalCountHeaderPagination
    ordering = ['-average_rating']  # default ordering

    def get_serializer_class(self):
        if self.action == 'list':
            return AnimeListSerializer
        if self.action == 'retrieve':
            return AnimeDetailSerializer


class AlgoliaIndexAPIView(generics.GenericAPIView):
    serializer_class = AnimeIndexSerializer
    queryset = Anime.objects.all()

    def get(self, request):
        """
        Algolia index API for Anime Model
        """
        query = request.GET.get('search')
        tag = request.GET.get('tag')
        search_result = perform_serach(query=query, tags=tag)
        return Response(search_result)


class AnimeCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment
    lookup_field = 'id'
    pagination_class = TotalCountHeaderPagination
    permission_cls = {
        'list': [permissions.AllowAny],
        'create': [permissions.IsAuthenticated],
        'partial_update': [permissions.IsAuthenticated],
        'destroy': [permissions.IsAuthenticated],
    }

    def get_permissions(self):
        try:
            return [
                permission() for permission in self.permission_cls[self.action]
            ]
        except KeyError:
            return [
                permission() for permission in self.permission_classes
            ]

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        if self.action == 'partial_update':
            return CommentUpdateSerializer
        if self.action == 'list':
            return CommentsListSerializer

    def list(self, request, *args, **kwargs):
        """
        Query param - id of anime;
        Retrieve list of all comments, related to anime instance;
        Orber by: created_at;
        """
        anime_id = kwargs.get('id')
        commentable = get_object_or_404(Anime, id=anime_id)
        comments = commentable.comments.all().order_by('created_at')
        page = self.paginate_queryset(comments)
        serializer = self.get_serializer(page, many=True)

        if not serializer.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Query param - id of anime;
        Request body - author(user_id, int), body(text, str);
        Authorization header required.
        """
        anime_id = kwargs.get('id')
        get_object_or_404(Anime, id=anime_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # * restriction from creating comment for another authors
        if request.user.id != serializer.data.get('author'):
            return Response(
                {'detail': 'You are not authorized to this action'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.create(serializer.data, anime_id)
        return Response(status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        """
        Allow to update body of comment instance for specific anime;
        Authorization header required.
        """
        anime_id = kwargs.get('id')
        comment_id = kwargs.get('comment_id')
        commentable = get_object_or_404(Anime, id=anime_id)
        comment = get_object_or_404(
            commentable.comments.all(),
            id=comment_id
        )

        if request.user.id != comment.author.id:
            return Response(
                {'detail': 'You are not authorized to this action'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(serializer.data, comment)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Allow to delete comment instance for specific anime;
        Authorization header required.
        """
        anime_id = kwargs.get('id')
        comment_id = kwargs.get('comment_id')
        commentable = get_object_or_404(Anime, id=anime_id)
        comment = get_object_or_404(
            commentable.comments.all(),
            id=comment_id
        )

        if request.user.id != comment.author.id:
            return Response(
                {'detail': 'You are not authorized to this action'},
                status=status.HTTP_403_FORBIDDEN
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnimeReviewViewSet(viewsets.ModelViewSet):
    queryset = Review
    permission_cls = {
        'list': [permissions.AllowAny],
        'create': [permissions.IsAuthenticated],
        'partial_update': [permissions.IsAuthenticated],
        'destroy': [permissions.IsAuthenticated],
    }

    def get_permissions(self):
        try:
            return [
                permission() for permission in self.permission_cls[self.action]
            ]
        except KeyError:
            return [
                permission() for permission in self.permission_classes
            ]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewListSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        return Response(status=status.HTTP_100_CONTINUE)