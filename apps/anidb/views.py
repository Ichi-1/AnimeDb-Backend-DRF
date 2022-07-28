from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import (
    IsAdminUser, 
    DjangoModelPermissionsOrAnonReadOnly,
    IsAuthenticatedOrReadOnly
)
from apps.anidb.models import Anime
from .api.serializers import (
    AnimeListSerializer, 
)
from rest_framework.decorators import action
from rest_framework.response import Response


class AnimeViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    
    # if i use get_queryset i can remove attribute queryset
    # but need to utilize param: router(basename='anime')
    queryset = Anime.objects.all() 
    serializer_class = AnimeListSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    
    def get_queryset(self):
        return Anime.objects.all().order_by('-average_rating')

    # @action(methods=['get'], detail='False')
    # def sort_by_rating(self, request):
    #     qs = Anime.objects.all().order_by('-average_rating')
    #     qs = self.serializer_class(qs)
    #     return Response({'Anime Sorted By Rating': qs})
    