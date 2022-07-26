from django.db import models


class Anime(models.Model):
    age_rating = models.CharField(max_length=5, verbose_name='Age Rating')
    age_rating_guide = models.CharField( max_length=50, verbose_name='Age Rating Guidence')
    average_rating = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Average Rating')
    description = models.TextField(verbose_name='Description')
    episode_count = models.IntegerField(verbose_name='Episodes count')
    episode_length = models.IntegerField(verbose_name='Episode length')
    poster_image = models.URLField(max_length=255, verbose_name='Poster URL')
    release_end_year = models.IntegerField(verbose_name='Airing end year', null=True)
    release_season = models.CharField(max_length=20, verbose_name='Realese season', null=True)
    release_start_year = models.IntegerField(verbose_name='Release year', null=True)
    show_type = models.CharField(max_length=10, verbose_name='Show Type')
    staff = models.TextField(verbose_name='Staff Team', null=True)
    studio = models.CharField(max_length=50, verbose_name='Studio', null=True)
    tags = models.TextField(verbose_name='Genres Tags', null=True)
    title_en = models.CharField(max_length=255, verbose_name='English title')
    title_ja_jp = models.CharField(max_length=255, verbose_name='Japan title')
    total_length = models.IntegerField(verbose_name='Total length')
    voice_actors = models.TextField(verbose_name='Voice Actors', null=True)
 
    class Meta:
        verbose_name = 'Anime'
        verbose_name_plural = 'Animes'
    
    def __str__(self):
        return f'{self.title_en} / {self.title_ja_jp}'


#* Rating & Reviews System Models

# class RatingStar(models.Model):
#     values = models.PositiveSmallIntegerField(default=0)

#     class Meta:
#         verbose_name = 'Rating star'
#         verbose_name_plural = 'Rating stars'

#     def __str__(self):
#         return self.values

# class Rating(models.Model):
#     star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='star')
#     anime = models.ForeignKey(Anime, on_delete=models.CASCADE, verbose_name='anime')
    
#     class Meta:
#         verbose_name = 'Users rating'
#         verbose_name_plural = 'Users'
    

#     def __str__(self):
#         return f'{self.star} - {self.anime}'

# class Reviews(models.Model):
#     email = models.EmailField()
#     name = models.CharField(max_length=255)
#     text = models.TextField(max_length=5000, verbose_name='Review')
#     anime = models.ForeignKey(
#         Anime, 
#         verbose_name='Anime', 
#         on_delete=models.CASCADE
#     )
#     parent = models.ForeignKey(
#         'self', 
#         verbose_name='parent', 
#         on_delete=models.SET_NULL, 
#         blank=True, 
#         null=True
#     )
    
#     class Meta:
#         verbose_name = 'Review'
#         verbose_name_plural = 'Reviews'
    
    
#     def __str__(self):
#         return f'{self.name} - {self.movie}'

