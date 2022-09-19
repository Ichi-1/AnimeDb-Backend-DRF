from apps.users.models import User
from django.core.validators import (
    MinLengthValidator as MinStr,
    MaxLengthValidator as MaxStr,
)
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from faker import Faker
from rest_framework import serializers as s, status
from rest_framework.response import Response
from .models import Comment, Review, MyList
from apps.anime_db.models import Anime, AnimeReview
from apps.manga_db.models import Manga, MangaReview


class AuthorSerializer(s.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nickname', 'avatar_url')

    avatar_url = s.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.URI)
    def get_avatar_url(self, user: dict) -> str:
        if user.avatar:
            return user.avatar.url
        return "No image assigned to object"


class CommentsListSerializer(s.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author', 'id', 'body', 'created_at', 'updated_at')

    author = AuthorSerializer()


class CommentCreateSerializer(s.Serializer):
    COMMENTABLE_TYPES = (
        ('manga', 'manga'),
        ('anime', 'anime'),
        ('review', 'review')
    )

    
    body = s.CharField(max_length=500, validators=[MinStr(20)])
    commentable_type = s.ChoiceField(choices=COMMENTABLE_TYPES)
    commentable_id = s.IntegerField()

    def create(self, commentalbe, author):
        body = self.validated_data['body']

        Comment(author=author, body=body, commentable=commentalbe).save()
        return Response(status=status.HTTP_201_CREATED)


class CommentUpdateSerializer(s.Serializer):
    body = s.CharField(max_length=500, validators=[MinStr(20)])

    def update(self, comment):
        body = self.validated_data['body']
        comment.body = body
        comment.save()


class ReviewCreateSerializer(s.Serializer):
    """
    Parent Review Serializer Schema
    Provide polymorhic creation for different type of reviewable object
    """
    REVIEWABLE_TYPES = (
        ("anime", "anime"),
        ("manga", "manga")
    )
    reviewable_type = s.ChoiceField(choices=REVIEWABLE_TYPES)
    reviewable_id = s.IntegerField()
    body = s.CharField(validators=[MinStr(100)])
    santiment = s.ChoiceField(choices=Review.Santiment.choices)

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


class ReviewUpdateSerializer(s.ModelSerializer):
    class Meta:
        model = Review
        fields = ("body", "santiment")


class MyListSerializer(s.Serializer):
    score = s.ChoiceField(choices=MyList.Score.choices, default=0)
    note  = s.CharField(default=Faker().text(), validators=[MaxStr(200)])


class ActivityCountSerializer(s.Serializer):
    comments = s.IntegerField()
    reviews  = s.IntegerField()