from apps.authentication.models import User
from django.core.validators import MinLengthValidator
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_polymorphic.serializers import PolymorphicSerializer
from .models import Comment, Review, MangaReview, AnimeReview


class AuthorSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.URI)
    def get_avatar_url(self, user: dict) -> str:
        if user.avatar:
            return user.avatar.url
        return "No image assigned to object"

    class Meta:
        model = User
        fields = ('id', 'nickname', 'avatar_url')


class CommentsListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Comment
        fields = ('author', 'id', 'body', 'created_at', 'updated_at')


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
        
        try:
            Comment(author=author, body=body, commentable=commentalbe).save()
            return Response(status=status.HTTP_201_CREATED)
        except BaseException:
            return Response(status=status.HTTP_418_IM_A_TEAPOT)


class CommentUpdateSerializer(serializers.Serializer):
    body = serializers.CharField(max_length=500, validators=[MinLengthValidator(20)])

    def update(self, comment):
        body = self.validated_data['body']
        comment.body = body
        comment.save()


class ReviewSerializer(serializers.Serializer):
    """
    Parent Review Serializer Schema
    """
    class Meta:
        model = Review
        fields = "__all__"


class AnimeReviewCreateSerializer(serializers.ModelSerializer):
    body = serializers.CharField(validators=[MinLengthValidator(100)])
    # child serializes should include resource_type_field_name to correct validation

    class Meta:
        model = AnimeReview
        fields = ("anime", "author", "body", "santiment")


class MangaReviewCreateSerializer(serializers.ModelSerializer):
    body = serializers.CharField(validators=[MinLengthValidator(100)])
    # child serializes should include resource_type_field_name to correct validation

    class Meta:
        model = MangaReview
        fields = ( "manga", "author", "body", "santiment")


class AnimeReviewListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = AnimeReview
        exclude = ("polymorphic_ctype", )


class MangaReviewListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = MangaReview
        exclude = ("polymorphic_ctype", )


class ReviewUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ("body", "santiment")


class ReviewPolymorhicSerializer(PolymorphicSerializer):
    resource_type_field_name = 'reviewable_type'

    model_serializer_mapping = {
        Review: ReviewSerializer,
        AnimeReview: AnimeReviewCreateSerializer,
        MangaReview: MangaReviewCreateSerializer,
    }

    def to_resource_type(self, model_or_instance):
        return super().to_resource_type(model_or_instance).lower()[:5]
    
    