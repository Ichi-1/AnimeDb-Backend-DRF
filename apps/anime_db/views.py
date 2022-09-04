from apps.activity.serializers import CommentsListSerializer
from apps.activity.models import Comment
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import mixins, generics, permissions, viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from .models import Anime
from .utils.algolia import perform_serach
from .utils.filterset import AnimeListFilter
from .utils.paging import TotalCountHeaderPagination
from .serializers import (
    AnimeDetailSerializer,
    AnimeIndexSerializer,
    AnimeListSerializer,
)
from apps.activity.paging import CommentListPaginator


class AnimeViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    GET /anime/ - retrieve list of all anime contained in database; Order by: average_rating
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


class AnimeCommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    lookup_field = 'id'
    pagination_class = CommentListPaginator
    permission_classes = [permissions.AllowAny]
    serializer_class = CommentsListSerializer

    def list(self, request, *args, **kwargs):
        """
        Query param - id of anime;
        Retrieve list of all comments, related to anime instance;
        orderBy: created_at;
        """
        anime_id = kwargs.get('id')
        commentable_anime = get_object_or_404(Anime, id=anime_id)
        comments = commentable_anime.comments.all().order_by('created_at')
        page = self.paginate_queryset(comments)
        serializer = self.get_serializer(page, many=True)

        if not serializer.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return self.get_paginated_response(serializer.data)

