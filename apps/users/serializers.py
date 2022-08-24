from rest_framework import serializers
from apps.authentication.models import CustomUser



class UserListSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

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



class UserMeRetrieveSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'nickname',
            'email',
            'avatar_url',
            'gender',
            'birthdate',
            'about'
        )
    
    def get_avatar_url(self, user):
        if user.avatar:
            return user.avatar.url
        else:
            return "No image assigned to object"



class UserMeUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    gender = serializers.CharField(required=False)
    birthdate = serializers.DateField(required=False)
    about = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('avatar', 'gender', 'birthdate', 'about')