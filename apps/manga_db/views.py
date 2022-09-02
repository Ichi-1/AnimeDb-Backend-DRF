from apps.anime_db.utils.paginator import TotalCountHeaderPagination
from django.shortcuts import render
from rest_framework import mixins, viewsets, permissions
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
    GET /manga/ - retrieve list of all manga contained in database; Order by: average_rating
    GET /manga/:id - retrieve instance of manga by id;
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