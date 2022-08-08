from django.urls import path, include

from djoser.views import UserViewSet

from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .utils.tokens import MyTokenObtainPairView
from .views import UserCreateView


app_name = 'auth'


urlpatterns = [
    path('sign-up/', UserViewSet.as_view({'post': 'create'})),
    path('activation/<str:uid>/<str:token>/', UserViewSet.as_view({'post': 'activation'})),
    path('activation-resend/', UserViewSet.as_view({'post': 'resend_activation'})),

    path('jwt/create/', MyTokenObtainPairView.as_view()),
    path('jwt/refresh/', TokenRefreshView.as_view()),
    path('jwt/verify/', TokenVerifyView.as_view()),

    # path('social/google/', )

    # path('reset-password/', UserViewSet.as_view({'post': 'reset_password'})),
    # path('reset-password-confirm/<str:uid>/<str:token>/',UserViewSet.as_view({'post': 'reset_password_confirm'})),
]

