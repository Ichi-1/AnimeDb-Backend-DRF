from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django.contrib.auth.models import update_last_login
# from drf_spectacular.utils import extend_schema_view, extend_schema


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print(user.avatar)

        # Add custom claims
        token['nickname'] = user.nickname
        token['avatar'] = f'{settings.STORAGE_URL}{user.avatar}'

        update_last_login(None, user=user)
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
