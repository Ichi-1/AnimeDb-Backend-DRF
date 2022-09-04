from apps.authentication.models import User
from generic_relations.relations import GenericRelatedField
from rest_framework import serializers, status
from rest_framework.response import Response
from .models import Comment, Review
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





# class ReviewListSerializer(serializers.ModelSerializer):

#     author = GenericRelatedField({
#         User: AuthorSerializer(),
#     })

#     class Meta:
#         model = Review
#         fields = (
#             'author', 
#             'id', 
#             'body',
#             'santiment',
#             'created_at', 
#             'updated_at'
#         )


# class FavoritesSerializer(serializers.Serializer):
#     FAVORITES_TYPE = (
#         ('manga', 'manga_db.Manga'),
#         ('anime', 'anime_db.Anime')
#     )
    
#     favorites_type = serializers.ChoiceField(choices=FAVORITES_TYPE)
#     favorites_id = serializers.IntegerField()

