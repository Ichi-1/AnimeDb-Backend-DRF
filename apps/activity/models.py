from apps.authentication.models import CustomUser
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Comment(models.Model):
    """
    Entity represent comments of different commentable models:
    reviews, anime, users profile etc.;
    """
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.DO_NOTHING,
        related_name='comments'
    )
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    commentable_id = models.PositiveIntegerField()
    commentable = GenericForeignKey('content_type', 'commentable_id')

    def __str__(self):
        return f'comment_id: {self.id}, commentable: {self.commentable}'


# class Review(models.Model):

#     SANTIMENT = (
#         ('Positive', 'Positive')
#         ('Neutral', 'Neutral')
#         ('Negative', 'Negative')
#     )

#     anime = models.ForeignKey(
#         Anime,
#         related_name='review',
#         on_delete=models.CASCADE
#     )
#     author = models.ForeignKey(
#         CustomUser,
#         related_name='review_author',
#         on_delete=models.CASCADE
#     )
#     body = models.TextField()
#     santiment = models.CharField(choices=SANTIMENT, max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
