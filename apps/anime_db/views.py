from apps.activity.models import Comment
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import mixins, generics, permissions, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from .models import Anime
from .utils.algolia import perform_serach
from .utils.filterset import AnimeListFilter
from .utils.paginator import TotalCountHeaderPagination
from .serializers import (
    AnimeSerializer,
    AnimeIndexSerializer,
    AnimeListSerializer,
)
from apps.activity.serializers import (
    CommentCreateSerializer,
    CommentsListSerializer
)

class AnimeViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):  
    """
    GET /anime/ - retrieve list of all anime contained in database;
    GET /anime/:id - retrieve instance of anime by id;
    """
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
            return AnimeSerializer


class AlgoliaIndexAPIView(generics.GenericAPIView):
    serializer_class = AnimeIndexSerializer
    queryset = Anime.objects.all()

    def get(self, request):
        """
        Algolia index API for Anime Model
        """
        query = request.GET.get('search')
        tag = request.GET.get('tag')
        search_result = perform_serach(query=query, tags=tag)
        return Response(search_result)


class AnimeCommentViewSet(viewsets.ModelViewSet):  
    queryset = Comment
    pagination_class = TotalCountHeaderPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        if self.action == 'list':
            return CommentsListSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """
        Retrieve list of all comments belonging to anime which id is passed in query. 
        Orber by: created_at
        """
        anime_id = kwargs.get('id')
        commentable = Anime.objects.get(id=anime_id)
        comments = commentable.comments.all().order_by('created_at')
        serializer = self.get_serializer(comments, many=True)

        if not serializer.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        """
        Query param - (id, int)
        Request body - author(user_id, int), body(text, str)
        Authorization header is required.
        """
        anime_id = kwargs.get('id')
        commentable = Anime.objects.filter(id=anime_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if request.user.id != serializer.data.get('author'):
            return Response(
                {'detail': 'You are not authorized to this action'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not commentable.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer.create_comment(serializer.data, anime_id)
        return Response(status=status.HTTP_201_CREATED)

