from apps.authentication.models import User
from django.core.validators import MinLengthValidator
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers, status
from rest_framework.response import Response
from .models import SANTIMENT, Comment, Review, MangaReview, AnimeReview
from apps.anime_db.models import Anime
from apps.manga_db.models import Manga


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nickname', 'avatar_url')

    avatar_url = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.URI)
    def get_avatar_url(self, user: dict) -> str:
        if user.avatar:
            return user.avatar.url
        return "No image assigned to object"


class CommentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author', 'id', 'body', 'created_at', 'updated_at')

    author = AuthorSerializer()


class CommentCreateSerializer(serializers.Serializer):
    COMMENTABLE_TYPES = (
        ('manga', 'manga'),
        ('anime', 'anime'),
        ('review', 'review')
    )
    body = serializers.CharField(max_length=500, validators=[MinLengthValidator(20)])
    commentable_type = serializers.ChoiceField(choices=COMMENTABLE_TYPES)
    commentable_id = serializers.IntegerField()

    def create(self, commentalbe, author):
        body = self.validated_data['body']

        Comment(author=author, body=body, commentable=commentalbe).save()
        return Response(status=status.HTTP_201_CREATED)


class CommentUpdateSerializer(serializers.Serializer):
    body = serializers.CharField(max_length=500, validators=[MinLengthValidator(20)])

    def update(self, comment):
        body = self.validated_data['body']
        comment.body = body
        comment.save()


class ReviewCreateSerializer(serializers.Serializer):
    """
    Parent Review Serializer Schema
    Provide polymorhic creation for different type of reviewable object
    """
    REVIEWABLE_TYPES = (
        ("anime", "anime"),
        ("manga", "manga")
    )
    reviewable_type = serializers.ChoiceField(choices=REVIEWABLE_TYPES)
    reviewable_id = serializers.IntegerField()
    body = serializers.CharField(validators=[MinLengthValidator(100)])
    santiment = serializers.ChoiceField(choices=SANTIMENT)

    def polymorhic_create(self, validated_data, author):
        reviewable_type = validated_data["reviewable_type"]
        reviewable_id = validated_data["reviewable_id"]

        if reviewable_type == "anime":
            anime = get_object_or_404(Anime, id=reviewable_id)
            AnimeReview(
                anime=anime,
                author=author,
                body=validated_data["body"],
                santiment=validated_data["santiment"]
            ).save()
            return Response(status=status.HTTP_201_CREATED)

        if reviewable_type == "manga":
            manga = get_object_or_404(Manga, id=reviewable_id)
            MangaReview(
                manga=manga,
                author=author,
                body=validated_data["body"],
                santiment=validated_data["santiment"]
            ).save()
            return Response(status=status.HTTP_201_CREATED)


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("body", "santiment")


class AnimeReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimeReview
        exclude = ("polymorphic_ctype", )

    author = AuthorSerializer()


class MangaReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MangaReview
        exclude = ("polymorphic_ctype", )

    author = AuthorSerializer()
