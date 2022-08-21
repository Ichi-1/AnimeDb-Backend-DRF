from rest_framework.serializers import ModelSerializer, SerializerMethodField
from apps.authentication.models import CustomUser



class UserListSerializer(ModelSerializer):
    avatar_url = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'nickname',
            'avatar_url',
            'last_login',
            'created_at',
        )

    def get_avatar_url(self, user):
        if user.avatar:
            return user.avatar.url
        else:
            return "No image assigned to object"



class UserMeSerializer(ModelSerializer):
    avatar_url = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'nickname',
            'email',
            'avatar_url',
            'gender',
            'birhdate',
            'about'
        )
    
    def get_avatar_url(self, user):
        if user.avatar:
            return user.avatar.url
        else:
            return "No image assigned to object"