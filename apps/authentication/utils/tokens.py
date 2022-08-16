from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

#TODO Add user avatar pics url to token claims 

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print(user.avatar)

        # Add custom claims
        token['nickname'] = user.nickname
        token['avatar'] = f'{settings.STORAGE_URL}{user.avatar}'
        # ...
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['nickname'] = user.nickname

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
