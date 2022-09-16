from django.contrib import admin
from .models import (
    Comment,
    Review,
)
from apps.anime_db.models import AnimeReview
from apps.manga_db.models import MangaReview
from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin
)


class CommentAdminConfig(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'content_type',
        'commentable',
        'commentable_id',
        'created_at',
    )


admin.site.register(Comment, CommentAdminConfig)


class ReviewChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Review  # Optional, explicitly set here.


@admin.register(AnimeReview)
class AnimeReviewAdmin(ReviewChildAdmin):
    base_model = AnimeReview  # Explicitly set here!
    list_display = ['id', 'author', 'anime', 'santiment', 'created_at']


@admin.register(MangaReview)
class MangaReviewAdmin(ReviewChildAdmin):
    base_model = MangaReview
    list_display = ['id', 'author', 'manga', 'santiment', 'created_at']


@admin.register(Review)
class ReviewParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = Review  # Optional, explicitly set here.
    child_models = [AnimeReview, MangaReview]
    list_display = ['id', 'author', 'polymorphic_ctype', 'santiment', 'created_at']
