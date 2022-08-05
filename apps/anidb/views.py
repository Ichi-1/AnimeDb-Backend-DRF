from apps.anidb.api.filters import AnimeFilter
from .api.serializers import AnimeListSerializer, AnimeDetailsSerializer
from apps.anidb.api.filterset import AnimeListFilter

from apps.anidb.models import Anime
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class AnimeViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

                   
    # 1. As list - return id, title_en, title_ja_jp, poster_image, average_rating.
    # 2. As retrieve - return all of the model instance fields.

    
    # if i use get_queryset i can remove attribute queryset
    # but need to utilize param: router(basename='anime')
    queryset = Anime.objects.all()
    permission_classes = [AllowAny]
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filterset_class = AnimeListFilter
    search_fields = ['title', '^title', 'year']
    ordering_fields = ['title', 'year', '?']
    ordering = ['-average_rating'] # default ordering
    

    def get_serializer_class(self):
        if self.action == 'list':
            return AnimeListSerializer
        if self.action == 'retrieve':
            return AnimeDetailsSerializer
    

    
