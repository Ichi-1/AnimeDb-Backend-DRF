from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Genre name')
    slug = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Anime(models.Model):
    uuid = models.CharField(primary_key=True, max_length=255)
    age_rating = models.CharField(max_length=5, verbose_name='Age Rating')
    age_rating_guide = models.CharField(max_length=50, verbose_name='Age Rating Guidence')
    average_rating = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Average Rating')
    description = models.TextField(verbose_name='Description')
    episode_count = models.IntegerField(verbose_name='Episodes count')
    episode_length = models.IntegerField(verbose_name='Episode length')
    poster_image = models.URLField(max_length=255, verbose_name='Poster URL')
    show_type = models.CharField(max_length=10, verbose_name='Show Type')
    title_en = models.CharField(max_length=255, verbose_name='English title')
    title_ja_jp = models.CharField(max_length=255, verbose_name='Japan title')
    total_length = models.IntegerField(verbose_name='Total length')
 

    def __str__(self):
        return f'{self.title_en} / {self.title_ja_jp}'
    
    class Meta:
        verbose_name = 'Anime Title'
        verbose_name_plural = 'Anime Titles'



class RatingStar(models.Model):
    values = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.values

    class Meta:
        verbose_name = 'Rating star'
        verbose_name_plural = 'Rating stars'



class AverageRating(models.Model):
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='star')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, verbose_name='anime')

    def __str__(self):
        return f'{self.star} - {self.anime}'
    
    class Meta:
        verbose_name = 'Average score'
        verbose_name_plural = 'Average scores'


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    text = models.TextField(max_length=5000, verbose_name='Review')
    anime = models.ForeignKey(
        Anime, 
        verbose_name='Anime', 
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        'self', 
        verbose_name='parent', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True
    )

    def __str__(self):
        return f'{self.name} - {self.movie}'
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

