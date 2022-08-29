from apps.anime_db.models import Anime
from apps.authentication.models import CustomUser
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)
from generic_relations.relations import GenericRelatedField
from .models import Comment


class CommentAuthorSerializer(ModelSerializer):
    avatar_url = SerializerMethodField()

    def get_avatar_url(self, user):
        if user.avatar:
            return user.avatar.url
        return "No image assigned to object"

    class Meta:
        model = CustomUser
        fields = ('nickname', 'avatar_url')


class CommentsListSerializer(ModelSerializer):

    author = GenericRelatedField({
        CustomUser: CommentAuthorSerializer(),
    })

    class Meta:
        model = Comment
        fields = ('author', 'body', 'created_at', 'updated_at')


class CommentCreateSerializer(ModelSerializer):

    def create(self, validated_data, anime_id):

        author = CustomUser.objects.get(id=validated_data['author'])
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
