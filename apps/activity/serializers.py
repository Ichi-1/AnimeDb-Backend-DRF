from apps.authentication.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_polymorphic.serializers import PolymorphicSerializer
from .models import Comment, Review, MangaReview, AnimeReview
from django.core.validators import MinLengthValidator
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

# from generic_relations.relations import GenericRelatedField


class AuthorSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.URI)
    def get_avatar_url(self, user: dict) -> str:
        if user.avatar:
            return user.avatar.url
        return "No image assigned to object"

    class Meta:
        model = User
        fields = ('id', 'nickname', 'avatar_url', )


class CommentsListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Comment
        fields = ('author', 'id', 'body', 'created_at', 'updated_at')


class CommentCreateSerializer(serializers.ModelSerializer):
    COMMENTABLE_TYPES = (
        ('Manga', 'Manga'),
        ('Anime', 'Anime'),
    )
    commentable_type = serializers.ChoiceField(choices=COMMENTABLE_TYPES)
    body = serializers.CharField(max_length=500, validators=[MinLengthValidator(20)])
    commentable_id = serializers.IntegerField()

    def create(self, commentalbe):
        author = self.validated_data['author']
        body = self.validated_data['body']

        try:
            Comment(author=author, body=body, commentable=commentalbe).save()
        except Exception:
            return Response(
                {"error": "Error during comment creation. Area: serializer"},
                status=status.HTTP_400_BAD_REQUEST
            )

    class Meta:
        model = Comment
        fields = ('author', 'body', 'commentable_type', 'commentable_id')


class CommentUpdateSerializer(serializers.ModelSerializer):

    body = serializers.CharField(max_length=500, validators=[MinLengthValidator(20)])

    def update(self, comment):
        body = self.validated_data['body']
        comment.body = body
        comment.save()

    class Meta:
        model = Comment
        fields = ('body',)


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
    
