from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView, 
    RetrieveDestroyAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import (
    IsAdminUser, 
    DjangoModelPermissionsOrAnonReadOnly,
    IsAuthenticatedOrReadOnly
)
from apps.anidb.models import Anime
from .serializers import (
    AnimeListSerializer, 
    AnimeDetailsSerializer,
)
    

class AnimeList(ListAPIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Anime.objects.all()[0:15]
    serializer_class = AnimeListSerializer

class AnimeDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Anime.objects.all()
    serializer_class = AnimeDetailsSerializer