from apps.anime_db.models import Anime
from apps.authentication.models import CustomUser
from rest_framework import serializers
from generic_relations.relations import GenericRelatedField
from .models import Comment


class CommentAuthorSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('nickname', 'avatar_url')

    def get_avatar_url(self, user):
        if user.avatar:
            return user.avatar.url
        return "No image assigned to object"


class CommentsListSerializer(serializers.ModelSerializer):
    
    author = GenericRelatedField({
        CustomUser: CommentAuthorSerializer(),
    })

    class Meta:
        model = Comment
        fields = (
            'author', 
            'body', 
            'created_at', 
            'updated_at',
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = (
            'author', 
            'body', 
        )
    
    def create_comment(self, validated_data, anime_id):
        
        author = CustomUser.objects.get(id=validated_data['author'])
        commentable = Anime.objects.get(id=anime_id)
        body = validated_data['body']

        try:
            Comment(author=author, commentable=commentable, body=body).save()
        except ValueError:
            raise serializers.ValidationError("Error during comment creation. Area: serializer")