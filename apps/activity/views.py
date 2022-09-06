from apps.anime_db.models import Anime
from apps.manga_db.models import Manga
from apps.authentication.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from .models import Comment, Review
from .serializers import (
    CommentCreateSerializer,
    CommentUpdateSerializer,
    ReviewPolymorhicSerializer
)



class CommentViewSet(ModelViewSet):
    """
    Attention! Look for possible commentable_type in request params
    Availiable commentable_type: "Manga", "Anime"
    """
    queryset = Comment
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        if self.action == 'partial_update':
            return CommentUpdateSerializer

    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        commentable_type = serializer.data['commentable_type']
        commentable_id = serializer.data['commentable_id']

        if commentable_type == 'Manga':
            commentable = get_object_or_404(Manga, id=commentable_id)
            serializer.create(commentable)
            return Response(status=status.HTTP_201_CREATED)

        if commentable_type == 'Anime':
            commentable = get_object_or_404(Anime, id=commentable_id)
            serializer.create(commentable)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_418_IM_A_TEAPOT)
        
    def partial_update(self, request, *args, **kwargs):
        """
         Authorization header required.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        comment_id = kwargs.get('id')
        comment = get_object_or_404(Comment,id=comment_id)

        if request.user.id != comment.author.id:
            return Response(
                {'detail': 'You are not authorized to this action'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.update(comment)
        return Response(status=status.HTTP_200_OK)

    
    def destroy(self, request, *args, **kwargs):
        """
        Authorization header required.
        """
        comment_id = kwargs.get('id')
        comment = get_object_or_404(Comment, id=comment_id)
        
        if request.user.id != comment.author.id:
            return Response(
                {'detail': 'You are not authorized to this action'},
                status=status.HTTP_403_FORBIDDEN
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewPolymorhicSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)