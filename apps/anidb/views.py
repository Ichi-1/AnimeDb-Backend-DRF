from .api.serializers import AnimeListSerializer, AnimeDetailsSerializer
from apps.anidb.api.filterset import AnimeListFilter
from apps.anidb.models import Anime

from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend


class TotalCountHeaderPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "count": self.page.paginator.count,
            "x-total-count": self.page.paginator.num_pages,
            "result": data
        })



class AnimeViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    # 1. As list - return id, title, title_jp, poster_image, average_rating
    # 2. As retrieve - return all of the model instance fields.

    # if i use get_queryset i can remove attribute queryset
    # but need to utilize param: router(basename='anime')
    queryset = Anime.objects.all()
    permission_classes = [AllowAny]
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
            return AnimeDetailsSerializer
