from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from apps.content_activity.models import Comment

class Anime(models.Model):
    id = models.AutoField(primary_key=True)
    age_rating = models.CharField(max_length=5, verbose_name='Age Rating')
    age_rating_guide = models.CharField(max_length=50, verbose_name='Age Rating Guidence')
    average_rating = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Average Rating')
    description = models.TextField(verbose_name='Description')
    episode_count = models.IntegerField(verbose_name='Episodes count')
    episode_length = models.IntegerField(verbose_name='Episode length')
    kind = models.CharField(max_length=10, verbose_name='Show Type')
    poster_image = models.URLField(max_length=255, verbose_name='Poster URL')
    season = models.CharField(max_length=20, verbose_name='Realese season', null=True)
    staff = models.TextField(verbose_name='Staff Team', null=True)
    studio = models.CharField(max_length=50, verbose_name='Studio', null=True)
    tags = models.TextField(verbose_name='Genres Tags', null=True)
    title = models.CharField(max_length=255, verbose_name='English title')
    title_jp = models.CharField(max_length=255, verbose_name='Japan title')
    total_length = models.IntegerField(verbose_name='Total length')
    voice_actors = models.TextField(verbose_name='Voice Actors', null=True)
    year = models.IntegerField(verbose_name='Release year', null=True)
    year_end = models.IntegerField(verbose_name='Airing end year', null=True)


    # comments = GenericRelation(Comment)

    class Meta:
        verbose_name = 'Anime'
        verbose_name_plural = 'Animes'

    def __str__(self):
        return f'{self.title} / {self.title_jp}'

    def get_tags_list(self):

        """ By now tags in model is text filed with enumaretiong of tag words.
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
