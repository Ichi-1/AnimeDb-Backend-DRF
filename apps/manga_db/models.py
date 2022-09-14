from apps.activity.models import Comment
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation


class Manga(models.Model):
    STATUS = (
        ('Finished', 'Finished'),
        ('On Hiatus', 'On Hiatus'),
        ('Publishing', 'Publishing'),
        ('Discontinued', 'Discontinued'),
    )

    id               = models.AutoField(primary_key=True)
    author           = models.TextField(verbose_name='Manga Author')
    average_rating   = models.FloatField(verbose_name='Average Rating')
    chapters         = models.PositiveIntegerField(verbose_name='Chapters count')
    description      = models.TextField(verbose_name='Description')
    media_type       = models.CharField(max_length=20)
    picture_main     = models.URLField(max_length=255, verbose_name='Poster URL')
    status           = models.CharField(choices=STATUS, max_length=20)
    tags             = models.TextField(verbose_name='Genres Tags', null=True)
    title            = models.CharField(max_length=255, verbose_name='English title')
    title_jp         = models.CharField(max_length=255, verbose_name='Japan title')
    volumes          = models.PositiveIntegerField(verbose_name='Volumes count')
    year_end         = models.DateTimeField(verbose_name='End year', null=True)
    year_start       = models.DateTimeField(verbose_name='Start year', null=True)
    # generic relation with comments, make manga commentable
    comments         = GenericRelation(Comment, object_id_field='commentable_id')
    # user favorites m2m
    user_favorites   = models.ManyToManyField(
        'authentication.User',
        related_name='favorites_manga',
        blank=True
    )

    def __str__(self):
        return self.title
