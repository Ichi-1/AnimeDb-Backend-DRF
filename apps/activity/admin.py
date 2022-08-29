from django.contrib import admin
from .models import Comment


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