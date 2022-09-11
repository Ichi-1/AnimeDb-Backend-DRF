from apps.authentication.models import User
from apps.anime_db.models import Anime
from apps.anime_db.utils.paging import TotalCountHeaderPagination
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
    ReviewUpdateSerializer,
    CommentsListSerializer
)
from drf_spectacular.utils import (
    extend_schema, 
    extend_schema_view,  
    OpenApiExample,
)


# TODO.Bug. Поле reviewable_type не отображается в сериализаторе по-умолчанию

class CommentView(ModelViewSet):
    """
    Availiable commentable_type: "manga", "anime", "review"
    """
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action == "create":
            return CommentCreateSerializer
        if self.action == "partial_update":
            return CommentUpdateSerializer
        
        return CommentCreateSerializer

    @extend_schema(
        summary="Create comment. Authorized Only",
        description="Appropriate commentable type must be set responsibly and explicitly"
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        author = get_object_or_404(User, id=serializer.data["author"])
        commentable_type = serializer.data["commentable_type"]
        commentable_id = serializer.data["commentable_id"]

        if commentable_type == "manga":
            commentable = get_object_or_404(Manga, id=commentable_id)
            return serializer.create(commentable, author)

        if commentable_type == "anime":
            commentable = get_object_or_404(Anime, id=commentable_id)
            return serializer.create(commentable, author)
        
        if commentable_type == "review":
            commentable = get_object_or_404(Review, id=commentable_id)
            return serializer.create(commentable, author)
        
        return Response(
            {"error": "Commentable type is not appropriate"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        summary="Update comment. Authorized Only",
        description="User can update comment which he is the author"
    )
    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment_id = kwargs.get("id")
        comment = get_object_or_404(Comment, id=comment_id)

        if request.user.id != comment.author.id:
            return Response(
                {"detail": "You are not authorized to this action"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.update(comment)
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete comment. Authorized Only",
        description="User can delete comment which he is the author"
    )
    def destroy(self, request, *args, **kwargs):
        comment_id = kwargs.get("id")
        comment = get_object_or_404(Comment, id=comment_id)

        if request.user.id != comment.author.id:
            return Response(
                {"detail": "You are not authorized to this action"},
                status=status.HTTP_403_FORBIDDEN
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@extend_schema_view(
    create=extend_schema(
        summary="Create review",
        examples=[
        OpenApiExample(
            name="AnimeReview",
            value={
                "reviewable_type": "anime",
                "anime": 1,
                "author": 1,
                "body": "Oh my god! This show is ridiculous!",
                "santiment": "Negative"
            },
        ),
        OpenApiExample(
            name="MangaReview",
            value={
                "reviewable_type": "manga",
                "manga": 1,
                "author": 1,
                "body": "Gosh! Cannot stop to read this masterpiece",
                "santiment": "Positive"
            },
        )]
    ),
    partial_update=extend_schema(summary="Update review"),
    destroy=extend_schema(summary="Delete review"),
)
class ReviewView(ModelViewSet):
    """
    Availiable reviewable_type: manga, anime.
    Authorized Only.
    """
    queryset = Review.objects.all().order_by("created_at")
    serializer_class = ReviewPolymorhicSerializer
    pagination_class = TotalCountHeaderPagination
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action == "partial_update":
            return ReviewUpdateSerializer
        return ReviewPolymorhicSerializer

    def partial_update(self, request, *args, **kwargs):
        review_id = kwargs.get("id")
        review = get_object_or_404(Review, pk=review_id)
        print(review)

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if request.user.id != review.author.id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, args, kwargs)


        
class ReviewCommentListView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsListSerializer
    pagination_class = TotalCountHeaderPagination
    lookup_field = "id"

    @extend_schema(
        summary="Get review comments list",
        description="If commentable resource has no comments empty list would returned"
    )
    def list(self, request, *args, **kwargs):
        review_id = kwargs.get("id")
        review = get_object_or_404(Review, pk=review_id)
        comments = review.comments.all().order_by("created_at")
        page = self.paginate_queryset(comments)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

        

    