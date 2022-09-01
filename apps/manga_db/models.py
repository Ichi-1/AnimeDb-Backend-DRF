from django.db import models
# from apps.authentication.models import CustomUser

class Manga(models.Model):
    STATUS = (
        ('Finished', 'Finished'),
        ('On Hiatus', 'On Hiatus'),
        ('Publishing', 'Publishing'),
    )

    average_rating   = models.FloatField(verbose_name='Average Rating')
    description      = models.TextField(verbose_name='Description')
    title            = models.CharField(max_length=255, verbose_name='English title')
    title_jp         = models.CharField(max_length=255, verbose_name='Japan title')
    picture_main     = models.URLField(max_length=255, verbose_name='Poster URL')
    status           = models.CharField(choices=STATUS, max_length=10)
    volumes          = models.PositiveIntegerField()
    chapters         = models.PositiveIntegerField()
    year_start       = models.IntegerField(verbose_name='Start year', null=True)
    genre            = models.CharField(max_length=15, verbose_name='Essential genre')
    # user_favourites  = models.ManyToManyField(CustomUser, related_name='favourites', blank=True)
