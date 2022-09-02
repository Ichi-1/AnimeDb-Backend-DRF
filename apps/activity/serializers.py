from apps.anime_db.models import Anime
from apps.authentication.models import User
from generic_relations.relations import GenericRelatedField
from rest_framework import serializers
from .models import Comment, Review


class CommentAuthorSerializer(serializers.ModelSerializer):
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
        User: CommentAuthorSerializer(),
    })

    class Meta:
        model = Comment
        fields = ('author', 'id', 'body', 'created_at', 'updated_at')


class CommentCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data, anime_id):
        author = User.objects.get(id=validated_data['author'])
        commentable = Anime.objects.get(id=anime_id)
        body = validated_data['body']

        try:
            Comment(author=author, commentable=commentable, body=body).save()
        except Exception:
            raise serializers.ValidationError(
                "Error during comment creation. Area: serializer"
            )

    class Meta:
        model = Comment
        fields = ('author', 'body')


class CommentUpdateSerializer(serializers.ModelSerializer):

    def update(self, validated_data, comment):
        body = validated_data['body']
        comment.body = body
        comment.save()

    class Meta:
        model = Comment
        fields = ('body',)





class ReviewListSerializer(serializers.ModelSerializer):

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
            'created_at', 
            'updated_at'
        )


class FavoritesSerializer(serializers.Serializer):
    FAVORITES_TYPE = (
        ('manga', 'manga_db.Manga'),
        ('anime', 'anime_db.Anime')
    )
    
    favorites_type = serializers.ChoiceField(choices=FAVORITES_TYPE)
    favorites_id = serializers.IntegerField()

