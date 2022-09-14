from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django.contrib.auth.models import update_last_login
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiExample


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


@extend_schema_view(
    post=extend_schema(
        summary='Create new JWT tokens pair for authenticated user',
        examples=[
            OpenApiExample(
                name="Anime Review",
                value={
                    "nickname": "admin",
                    "password": "admin"
                },
                request_only=True
            ),
        ],
        responses=TokenRefreshSerializer
    )
)
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
