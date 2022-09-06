from apps.authentication.models import User
from generic_relations.relations import GenericRelatedField
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_polymorphic.serializers import PolymorphicSerializer
from .models import Comment, Review, MangaReview, AnimeReview
from django.core.validators import MinLengthValidator


class AuthorSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    def get_avatar_url(self, user):
        if user.avatar:
            return user.avatar.url
        return "No image assigned to object"

    class Meta:
        model = User
        fields = ('id', 'nickname', 'avatar_url', )


class CommentsListSerializer(serializers.ModelSerializer):

    author = GenericRelatedField({
        User: AuthorSerializer(),
    })

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



class ReviewSerializer(serializers.ModelSerializer):

    author = AuthorSerializer()
    body = serializers.CharField(validators=[MinLengthValidator(100)])

    class Meta:
        model = Review
        fields = ("author", "body", "santiment")


class AnimeReviewSerialize(serializers.ModelSerializer):

    author = AuthorSerializer()
    body = serializers.CharField(validators=[MinLengthValidator(100)])

    class Meta:
        model = AnimeReview
        fields = ("anime", "author", "body", "santiment")


class MangaReviewSerialize(serializers.ModelSerializer):

    author = AuthorSerializer()
    body = serializers.CharField(validators=[MinLengthValidator(100)])

    class Meta:
        model = MangaReview
        fields = ("manga", "author", "body", "santiment")
    

class ReviewPolymorhicSerializer(PolymorphicSerializer):
    resource_type_field_name = "review_type"

    model_serializer_mapping = {
        Review: ReviewSerializer,
        AnimeReview: AnimeReviewSerialize,
        MangaReview: MangaReviewSerialize
    }


    def to_resource_type(self, model_or_instance):
        return model_or_instance._meta.object_name.lower()