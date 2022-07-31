from apps.anidb.models import Anime
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import (AllowAny)
from .api.serializers import (
    AnimeListSerializer, 
    AnimeDetailsSerializer,
)
from apps.anidb.api.filters import AnimeFilter
from django_filters import rest_framework as filters


class AnimeViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
                   
    # 1. As list - return id, title_en, title_ja_jp, poster_image, average_rating.
    # By default, sorted by average_rating desc.

    # 2. As retrieve - return all of the model instance fields.

    
    # if i use get_queryset i can remove attribute queryset
    # but need to utilize param: router(basename='anime')
    permission_classes = [AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AnimeFilter
    

    def get_serializer_class(self):
        if self.action == 'list':
            return AnimeListSerializer
        if self.action == 'retrieve':
            return AnimeDetailsSerializer
    
    def get_queryset(self):
        return Anime.objects.all().order_by('-average_rating')
    
