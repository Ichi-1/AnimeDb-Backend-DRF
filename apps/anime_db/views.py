from apps.activity.serializers import CommentsListSerializer, AnimeReviewListSerializer
from apps.activity.models import AnimeReview, Comment
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

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



@extend_schema_view(
    list=extend_schema(summary='Get anime list'),
    retrieve=extend_schema(summary='Get anime details')
)
class AnimeView(ModelViewSet):
    queryset = Anime.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filterset_class = AnimeListFilter
    search_fields = ['title', '^title', 'year']
    ordering_fields = ['title', 'year', '?']
    pagination_class = TotalCountHeaderPagination
    ordering = ['-average_rating']  # default ordering
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action == 'list':
            return AnimeListSerializer
        if self.action == 'retrieve':
            return AnimeDetailSerializer


class AlgoliaIndexAPIView(generics.GenericAPIView):
    queryset = Anime.objects.all()
    serializer_class = AnimeIndexSerializer

    @extend_schema(
        summary='JSON example of Algolia Search Index Result',
        description='Not for public use. Schema is not appropriate'
    )
    def get(self, request):
        query = request.GET.get('search')
        tag = request.GET.get('tag')
        search_result = perform_serach(query=query, tags=tag)
        return Response(search_result)


class AnimeCommentsView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CommentListPaginator
    lookup_field = "id"

    @extend_schema(
        summary="Get list of anime comments",
        description="If commentable resource has no comments empty list would returned"
    )
    def list(self, request, *args, **kwargs):
        anime_id = kwargs.get('id')
        commentable_anime = get_object_or_404(Anime, id=anime_id)
        comments = commentable_anime.comments.all().order_by('created_at')
        page = self.paginate_queryset(comments)
        serializer = self.get_serializer(page, many=True)
        # TODO Если комментариев к ресурсу нет - возвращается пустой массив
        return self.get_paginated_response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary='Get list of anime reviews')
)
class AnimeReviewView(ModelViewSet):
    queryset = AnimeReview.objects.all()
    serializer_class = AnimeReviewListSerializer
