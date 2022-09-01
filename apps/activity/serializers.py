from apps.anime_db.models import Anime
from apps.authentication.models import User
from generic_relations.relations import GenericRelatedField
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)
from .models import Comment, Review


class CommentAuthorSerializer(ModelSerializer):
    avatar_url = SerializerMethodField()

    def get_avatar_url(self, user):
        if user.avatar:
            return user.avatar.url
        return "No image assigned to object"

    class Meta:
        model = User
        fields = ('id', 'nickname', 'avatar_url', )


class CommentsListSerializer(ModelSerializer):

    author = GenericRelatedField({
        User: CommentAuthorSerializer(),
    })

    class Meta:
        model = Comment
        fields = ('author', 'id', 'body', 'created_at', 'updated_at')


class CommentCreateSerializer(ModelSerializer):

    def create(self, validated_data, anime_id):
        author = User.objects.get(id=validated_data['author'])
        commentable = Anime.objects.get(id=anime_id)
        body = validated_data['body']

        try:
            Comment(author=author, commentable=commentable, body=body).save()
        except Exception:
            raise ValidationError(
                "Error during comment creation. Area: serializer"
            )

    class Meta:
        model = Comment
        fields = ('author', 'body')


class CommentUpdateSerializer(ModelSerializer):

    def update(self, validated_data, comment):
        body = validated_data['body']
        comment.body = body
        comment.save()

    class Meta:
        model = Comment
        fields = ('body',)





class ReviewListSerializer(ModelSerializer):

    author = GenericRelatedField({
        User: CommentAuthorSerializer(),
    })

    class Meta:
        model = Review
        fields = (
            'author', 
            'id', 
            'body',
            'santiment',
            'votes_up_count',
            'votes_down_count',
            'created_at', 
            'updated_at'
        )