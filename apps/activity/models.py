from apps.authentication.models import User
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from polymorphic.models import PolymorphicModel


SANTIMENT = (
    ('Positive', 'Positive'),
    ('Neutral', 'Neutral'),
    ('Negative', 'Negative'),
)


class Comment(models.Model):
    """
    Entity represent comments of different commentable models:
    reviews, anime, users profile etc.;
    """
    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='comments'
    )
    body            = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    #
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    commentable     = GenericForeignKey('content_type', 'commentable_id')
    commentable_id  = models.PositiveIntegerField()

    def __str__(self):
        return f'comment_id: {self.id}, commentable: {self.commentable}'


class Review(PolymorphicModel):
    """
    Main difference from comment is "santiment" field.

    A review is a statement based on the expression of a personal
    emotional and evaluative attitude to a viewed or read title.
    (This is an opinion about the title, analysis, analysis, evaluation)
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='review_author',
        on_delete=models.DO_NOTHING,
    )
    body              = models.TextField()
    comments          = GenericRelation(Comment, object_id_field='commentable_id')
    santiment         = models.CharField(choices=SANTIMENT, max_length=10)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"Author: {self.author.nickname}, "
                f"Reviewable: {self.polymorphic_ctype}")

    def get_reviewable_type(self):
        """
        Возвращает тип reviewable объекта
        Варианты - anime, manga
        """
        return self.polymorphic_ctype


class AnimeReview(Review):
    anime = models.ForeignKey(
        'anime_db.Anime',
        blank=True,
        null=True,
        related_name='anime_review',
        on_delete=models.CASCADE,
    )


class MangaReview(Review):
    manga = models.ForeignKey(
        'manga_db.Manga',
        blank=True,
        null=True,
        related_name='manga_review',
        on_delete=models.CASCADE,
    )


# class Favorites(models.Model):

#     FAVORITES_TYPE = (
#         ('manga', 'manga_db.Manga'),
#         ('anime', 'anime_db.Anime')
#     )

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         related_name='favorites',
#         on_delete=models.CASCADE
#     )
#     favorites_type    = models.ForeignKey(choices=FAVORITES_TYPE, max_length=5, null=False, on_delete=)
#     favorites_id      = models.IntegerField('self.favorites_type.pk', null=False)
#     created_at        = models.DateTimeField(auto_now_add=True)
#     updated_at        = models.DateTimeField(auto_now=True)



