from django.contrib import admin
from .models import Comment, Review, AnimeReview, MangaReview
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
    # define custom features here


@admin.register(MangaReview)
class MangaReview(AnimeReviewAdmin):
    base_model = MangaReview


@admin.register(Review)
class ReviewParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = Review  # Optional, explicitly set here.
    child_models = [AnimeReview, MangaReview]
