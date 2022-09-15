from django.urls import path
from djoser.views import UserViewSet as Djoser
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .tokens import MyTokenObtainPairView
from .views import GoogleLoginAPIView, GitHubLoginAPIView

app_name = 'auth'

#   TODO В отдельный api_router выносятся вью содержащие более 1го метода в 1 роуте

urlpatterns = [
    path('sign-up/', Djoser.as_view({'post': 'create'})),
    path('activation/<str:uid>/<str:token>/', Djoser.as_view({'post': 'activation'})),
    path('activation-resend/', Djoser.as_view({'post': 'resend_activation'})),

    path('jwt/create/', MyTokenObtainPairView.as_view(), name='jwt_create_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view()),
    path('jwt/verify/', TokenVerifyView.as_view()),

    path('social/google/', GoogleLoginAPIView.as_view()),
    path('social/github/', GitHubLoginAPIView.as_view()),
    # path('djoser/', include('djoser.urls'))
]
