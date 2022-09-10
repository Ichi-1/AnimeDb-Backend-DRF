from apps.anime_db.models import Anime
from apps.manga_db.models import Manga
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Comment, Review
from .serializers import (
    CommentCreateSerializer,
    CommentUpdateSerializer,
    ReviewPolymorhicSerializer,
)

from drf_spectacular.utils import extend_schema  # PolymorphicProxySerializer


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
        else:
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


class ReviewViewSet(ModelViewSet):
    """
    Availiable review_type: "manga", "anime"
    """
    queryset = Review.objects.all()
    lookup_field = "id"
    serializer_class = ReviewPolymorhicSerializer

    # @extend_schema(
    #     request=PolymorphicProxySerializer(
    #         component_name='review_type',
    #         serializers=[
    #             AnimeReviewSerializer, MangaReviewSerializer
    #         ],
    #         resource_type_field_name='review_type',
    #     ),
    # )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
