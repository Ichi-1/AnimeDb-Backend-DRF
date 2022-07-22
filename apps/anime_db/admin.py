from django.contrib import admin

from .models import (
    Anime, AverageRating, Genre, RatingStar, Reviews
)

admin.site.register(Anime)
admin.site.register(AverageRating)
admin.site.register(Genre)
admin.site.register(RatingStar)
admin.site.register(Reviews)