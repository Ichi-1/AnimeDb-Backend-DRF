from apps.anime_db.models import Anime
from apps.manga_db.models import Manga
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from polymorphic.models import PolymorphicModel
from django.core.validators import (
    MaxValueValidator as MaxInt,
    MinLengthValidator as MinStr,
)


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
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='comments'
    )
    body            = models.TextField(validators=[MinStr(20)])
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    #
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    commentable     = GenericForeignKey('content_type', 'commentable_id')
    commentable_id  = models.PositiveIntegerField()

    def __str__(self):
        return f'comment_id: {self.id}, commentable: {self.commentable}'


# Reviews

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
    body              = models.TextField(validators=[MinStr(200)])
    santiment         = models.CharField(choices=SANTIMENT, max_length=10)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)
    comments          = GenericRelation(Comment, object_id_field='commentable_id')

    def __str__(self):
        return "Review"

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


# My List

class MyList(models.Model):
    class Meta:
        abstract = True

    class Score(models.IntegerChoices):
        AWFUL       = 1
        PRETTY_BAD  = 2
        SO_SO       = 3
        GOOD        = 4
        MASTERPIECE = 5

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s",
    )
    score = models.PositiveIntegerField(
        choices=Score.choices,
        verbose_name="Item score in list",
        default=0
    )
    note       = models.TextField(max_length=300, verbose_name="My note about item")
    updated_at = models.DateTimeField(auto_now=True)


class MyAnimeList(MyList):

    class ListStatus(models.Choices):
        watching      = "Watching"
        plan_to_watch = "Plan to watch"
        completed     = "Completed"
        dropped       = "Dropped"

    anime  = models.ForeignKey(Anime, on_delete=models.CASCADE)
    status = models.CharField(choices=ListStatus.choices, max_length=15)
    num_episodes_watched = models.PositiveIntegerField(
        validators=[MaxInt(100)],
        default=0,
        verbose_name="Number of watched episodes"
    )


class MyMangaList(MyList):

    class ListStatus(models.Choices):
        reading      = "Reading"
        plat_to_read = "Plan to read"
        completed    = "Completed"
        dropped      = "Dropped"

    manga  = models.ForeignKey(Manga, on_delete=models.CASCADE)
    status = models.CharField(choices=ListStatus.choices, max_length=15)
    num_chapters_read = models.PositiveIntegerField(
        validators=[MaxInt(7774)],
        default=0,
        verbose_name="Number of readed chapters"
    )
