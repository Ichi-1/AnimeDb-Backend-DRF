from rest_framework.serializers import ModelSerializer
from apps.blog.models import Post


class PostSerializer(ModelSerializer):
    
    class Meta:
        model = Post
        fields = (
            'id', 
            'title',
            'author', 
            'annotation', 
            'content', 
            'status',
        )