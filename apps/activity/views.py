from apps.anime_db.models import Anime
from apps.manga_db.models import Manga
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Comment, Review
from .serializers import (
    AnimeReviewCreateSerializer,
    CommentCreateSerializer,
    CommentUpdateSerializer,
    MangaReviewCreateSerializer,
    ReviewPolymorhicSerializer,
    ReviewUpdateSerializer
)

from drf_spectacular.utils import (
    extend_schema, 
    extend_schema_view,  
    OpenApiExample
)


class CommentViewSet(ModelViewSet):
    """
    Availiable commentable_type: "Manga", "Anime"
    """
    queryset = Comment.objects.all()
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        if self.action == 'partial_update':
            return CommentUpdateSerializer
        
        return CommentCreateSerializer

    @extend_schema(
        summary='Create comment. Authorized Only',
        description='Appropriate commentable type must be set responsibly and explicitly'
    )
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

    @extend_schema(
        summary='Update comment. Authorized Only',
        description='User can update comment which he is the author'
    )
    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment_id = kwargs.get('id')
        comment = get_object_or_404(Comment, id=comment_id)

        if request.user.id != comment.author.id:
            return Response(
                {'detail': 'You are not authorized to this action'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.update(comment)
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        summary='Delete comment. Authorized Only',
        description='User can delete comment which he is the author'
    )
    def destroy(self, request, *args, **kwargs):
        comment_id = kwargs.get('id')
        comment = get_object_or_404(Comment, id=comment_id)

        if request.user.id != comment.author.id:
            return Response(
                {'detail': 'You are not authorized to this action'},
                status=status.HTTP_403_FORBIDDEN
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@extend_schema_view(
    create=extend_schema(
        summary='Create review',
        examples=[
        OpenApiExample(
            name='AnimeReview',
            value={
                "reviewable_type": "anime",
                "anime": 1,
                "author": 1,
                "body": "Oh my god! This show is ridiculous!",
                "santiment": "Negative"
            },
        ),
        OpenApiExample(
            name='MangaReview',
            value={
                "reviewable_type": "manga",
                "manga": 1,
                "author": 1,
                "body": "Gosh! Cannot stop to read this masterpiece",
                "santiment": "Positive"
            },
        )]
    ),
    partial_update=extend_schema(summary='Update review'),
    destroy=extend_schema(summary='Delete review')
)
class ReviewViewSet(ModelViewSet):
    """
    Availiable reviewable_type: manga, anime.
    Authorized Only.
    """
    queryset = Review.objects.all()
    lookup_field = "id"
    serializer_class = ReviewPolymorhicSerializer

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ReviewUpdateSerializer
        return ReviewPolymorhicSerializer

    def partial_update(self, request, *args, **kwargs):
        review_id = kwargs.get('id')
        review = get_object_or_404(Review, pk=id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.id != review.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        return super().partial_update(request, args, kwargs)




