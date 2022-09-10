from apps.activity.serializers import CommentsListSerializer, MangaReviewListSerializer
from apps.anime_db.utils.paging import TotalCountHeaderPagination
from apps.activity.models import Comment, MangaReview
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins, permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Manga
from .serializers import (
    MangaDetailSerializer,
    MangaListSerializer
)


@extend_schema_view(
    list=extend_schema(summary='Get manga list'),
    retrieve=extend_schema(summary='Get manga details')
)
class MangaViewSet(ModelViewSet):
    queryset = Manga.objects.all()
    permission_classes = [permissions.AllowAny]
    pagination_class = TotalCountHeaderPagination
    ordering = ['-average_rating']  # default ordering

    def get_serializer_class(self):
        if self.action == 'list':
            return MangaListSerializer
        if self.action == 'retrieve':
            return MangaDetailSerializer


class MangaCommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    lookup_field = 'id'
    pagination_class = TotalCountHeaderPagination
    permission_classes = [permissions.AllowAny]
    serializer_class = CommentsListSerializer

    @extend_schema(summary='Get manga comments list')
    def list(self, request, *args, **kwargs):
        manga_id = kwargs.get('id')
        commentable_manga = get_object_or_404(Manga, id=manga_id)
        comments = commentable_manga.comments.all().order_by('created_at')
        page = self.paginate_queryset(comments)
        serializer = self.get_serializer(page, many=True)

        if not serializer.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return self.get_paginated_response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary="Get manga reviews list")
)
class MangaReviewsViewSet(ModelViewSet):
    queryset = MangaReview.objects.all()
    serializer_class =  MangaReviewListSerializer

