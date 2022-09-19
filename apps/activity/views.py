from apps.anime_db.models import Anime
from apps.anime_db.utils.paging import TotalCountHeaderPagination
from apps.manga_db.models import Manga
from apps.users.models import User
from django.shortcuts import get_object_or_404
from faker import Faker
from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Comment, Review
from .serializers import (
    CommentCreateSerializer,
    CommentUpdateSerializer,
    ReviewCreateSerializer,
    ReviewUpdateSerializer,
    CommentsListSerializer
)
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
)


@extend_schema_view(
    create=extend_schema(
        summary="Create comment. Authorized Only",
        description=(
            "Valid commentable type: "
            "```manga```, ```anime```, ```review```"
        )
    ),
    partial_update=extend_schema(
        summary="Update my comment. Authorized Only",
        description="User can update comment if he is author of"
    ),
    destroy=extend_schema(
        summary="Delete my comment. Authorized Only",
        description="User can delete comment if he is author of"
    )
)
class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action == "create":
            return CommentCreateSerializer
        if self.action == "partial_update":
            return CommentUpdateSerializer

        return CommentCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        author = get_object_or_404(User, id=request.user.id)
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


# TODO seiralizer.data['author'] = request.user.id
# TODO serializer.create()

@extend_schema_view(
    create=extend_schema(
        summary="Create review. Authorized Only.",
        description=(
            "Valid reviewable type: "
            "```anime```, ```manga```"
        ),
        examples=[
            OpenApiExample(
                name="Anime Review",
                value={
                    "reviewable_type": "anime",
                    "reviewable_id": 1,
                    "body": Faker().text(),
                    "santiment": "Negative"
                }
            ),
            OpenApiExample(
                name="Manga Review",
                value={
                    "reviewable_type": "manga",
                    "reviewable_id": 1,
                    "body": Faker().text(),
                    "santiment": "Positive"
                }
            )
        ]
    ),
    partial_update=extend_schema(
        summary="Update my review",
        description="User can update review if he is author of"
    ),
    destroy=extend_schema(
        summary="Delete my review",
        description="User can delete review if he is the author of",
    )
)
class ReviewView(ModelViewSet):
    queryset = Review.objects.all().order_by("created_at")
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action == "create":
            return ReviewCreateSerializer
        if self.action == "partial_update":
            return ReviewUpdateSerializer
        return ReviewCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = get_object_or_404(User, id=request.user.id)
        return serializer.polymorhic_create(serializer.data, author=author)

    def partial_update(self, request, *args, **kwargs):
        review_id = kwargs.get("id")
        review = get_object_or_404(Review, pk=review_id)

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if request.user.id != review.author.id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        review_id = kwargs.get("id")
        review = get_object_or_404(Review, pk=review_id)

        if request.user.id != review.author.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    list=extend_schema(
        summary="Get review comments list",
        description=(
            "If review has no comments"
            "empty list would be returned ```200```"
        )
    )
)
class ReviewCommentsListView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsListSerializer
    pagination_class = TotalCountHeaderPagination
    lookup_field = "id"

    def list(self, request, *args, **kwargs):
        review_id = kwargs.get("id")
        review = get_object_or_404(Review, pk=review_id)
        comments = review.comments.all().order_by("created_at")
        page = self.paginate_queryset(comments)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
