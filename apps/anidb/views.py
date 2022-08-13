from .api.algolia import perform_serach
from .api.filterset import AnimeListFilter
from .models import Anime
from .serializers import (
    AnimeDetailsSerializer,
    AnimeIndexSerializer,
    AnimeListSerializer, 
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    mixins, status, generics, 
    permissions, viewsets
)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


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
                   viewsets.GenericViewSet):
    # 1. As list - return id, title, title_jp, poster_image, average_rating
    # 2. As retrieve - return all of the model instance fields.

    # if i use get_queryset i can remove attribute queryset
    # but need to utilize param: router(basename='anime')
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
            return AnimeDetailsSerializer
    


class IndexAPIView(generics.GenericAPIView):
    serializer_class = AnimeIndexSerializer
    queryset = Anime
    
    def get(self, request):
        query = request.GET.get('search')
        tag = request.GET.get('tag')
        search_result = perform_serach(query=query, tags=tag)
        return Response(search_result)
