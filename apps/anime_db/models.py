from apps.activity.models import MyList, Review
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MaxValueValidator as MaxInt
from django.db import models


class Anime(models.Model):
    class Meta:
        verbose_name = 'Anime'
        verbose_name_plural = 'Anime'

    id               = models.AutoField(primary_key=True)
    age_rating       = models.CharField(max_length=5, verbose_name='Age Rating')
    age_rating_guide = models.CharField(max_length=50, verbose_name='Age Rating Guidence')
    average_rating   = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Average Rating')
    description      = models.TextField(verbose_name='Description')
    episode_count    = models.IntegerField(verbose_name='Episodes count')
    episode_length   = models.IntegerField(verbose_name='Episode length')
    kind             = models.CharField(max_length=10, verbose_name='Show Type')
    poster_image     = models.URLField(max_length=255, verbose_name='Poster URL')
    season           = models.CharField(max_length=20, verbose_name='Realese season', null=True)
    staff            = models.TextField(verbose_name='Staff Team', null=True)
    studio           = models.CharField(max_length=50, verbose_name='Studio', null=True)
    tags             = models.TextField(verbose_name='Genres Tags', null=True)
    title            = models.CharField(max_length=255, verbose_name='English title')
    title_jp         = models.CharField(max_length=255, verbose_name='Japan title')
    total_length     = models.IntegerField(verbose_name='Total length')
    voice_actors     = models.TextField(verbose_name='Voice Actors', null=True)
    year             = models.PositiveIntegerField(verbose_name='Release year', null=True)
    year_end         = models.PositiveIntegerField(verbose_name='Airing end year', null=True)
    # generic comments table
    comments         = GenericRelation("activity.Comment", object_id_field='commentable_id')
    # m2m user favourites anime
    user_favorites   = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorites_anime',
        blank=True
    )

    def __str__(self):
        return f'{self.title}'

    def get_tags_list(self):

        """
        By now "tags" in model is text filed with enumaretiong of tag words.
        Search engin suppose that filed is array conaining only one string,
        but it should be array of string, representig genres tags.
        """
        tags = self.tags

        #   WARNING: some filed is null
        if tags is None:
            return [self.tags]
        else:
            return ''.join(self.tags).split()

    @property
    def path(self):
        return f'/animes/{self.pk}/'


class AnimeReview(Review):
    anime = models.ForeignKey(
        'anime_db.Anime',
        blank=True,
        null=True,
        related_name='anime_review',
        on_delete=models.CASCADE,
    )


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
        null=True,
        verbose_name="Number of watched episodes"
    )
