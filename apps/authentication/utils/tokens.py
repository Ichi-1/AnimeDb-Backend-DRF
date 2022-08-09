import jwt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['nickname'] = user.nickname
        # ...
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




def get_tokens_for_user(user):
    
    refresh = RefreshToken.for_user(user)
    decodeJWT = jwt.decode(jwt=str(refresh), key=settings.SECRET_KEY, algorithms='HS256')
    print(decodeJWT)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }