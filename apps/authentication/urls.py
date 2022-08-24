from django.urls import path
from djoser.views import UserViewSet as DjoserViewSet
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .utils.tokens import MyTokenObtainPairView

app_name = 'auth'


urlpatterns = [
    path('sign-up/', DjoserViewSet.as_view({'post': 'create'})),
    path('activation/<str:uid>/<str:token>/', DjoserViewSet.as_view({'post': 'activation'})),
    path('activation-resend/', DjoserViewSet.as_view({'post': 'resend_activation'})),


    path('jwt/create/', MyTokenObtainPairView.as_view()),
    path('jwt/refresh/', TokenRefreshView.as_view()),
    path('jwt/verify/', TokenVerifyView.as_view()),


    
]
