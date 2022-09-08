from apps.activity.serializers import CommentsListSerializer
from apps.anime_db.utils.paging import TotalCountHeaderPagination
from apps.activity.models import Comment
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.response import Response
from .models import Manga
from .serializers import (
    MangaDetailSerializer,
    MangaListSerializer
)


class MangaViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    GET /manga/ - retrieve list of all manga contained in database;
    GET /manga/:id - retrieve instance of manga by id;
    orderBy: average_rating
    """
    queryset = Manga.objects.all()
    permission_classes = [permissions.AllowAny]
    pagination_class = TotalCountHeaderPagination
    ordering = ['-average_rating']  # default ordering

    def get_serializer_class(self):
        if self.action == 'list':
            return MangaListSerializer
        if self.action == 'retrieve':
            return MangaDetailSerializer


class MangaCommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment
    lookup_field = 'id'
    pagination_class = TotalCountHeaderPagination
    permission_classes = [permissions.AllowAny]
    serializer_class = CommentsListSerializer

    def list(self, request, *args, **kwargs):
        """
        Query param - id of manga;
        Retrieve list of all comments, related to manga instance;
        orderBy: created_at;
        """
        manga_id = kwargs.get('id')
        commentable_manga = get_object_or_404(Manga, id=manga_id)
        comments = commentable_manga.comments.all().order_by('created_at')
        page = self.paginate_queryset(comments)
        serializer = self.get_serializer(page, many=True)

        if not serializer.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return self.get_paginated_response(serializer.data)
