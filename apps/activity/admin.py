from django.contrib import admin
from .models import Comment, Review


class CommentAdminConfig(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'content_type',
        'commentable',
        'commentable_id',
        'created_at',
    )
class ReviewAdminConfig(admin.ModelAdmin):
    list_display = (
        'anime',
        'manga',
        'author',
        'body',
        'santiment',
        'created_at',
        'updated_at',
    )



admin.site.register(Comment, CommentAdminConfig)
admin.site.register(Review, ReviewAdminConfig)


