from django.contrib import admin

from .models import (
    Anime, 
    GenresTagList, 
    ReleaseInfo,
    
    RatingStar, 
    Rating, 
    Reviews 
)

admin.site.register(Anime)
admin.site.register(GenresTagList)
admin.site.register(ReleaseInfo)
admin.site.register(RatingStar)
admin.site.register(Reviews)
admin.site.register(Rating)