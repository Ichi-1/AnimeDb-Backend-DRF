from django.urls import path, include
from .views import UserCreateView
from rest_framework import routers

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .utils.tokens import MyTokenObtainPairView

router = routers.SimpleRouter()
router.register(r'users', UserCreateView)
app_name = 'users'


urlpatterns = [
    path('', include(router.urls)),
    path('jwt/', MyTokenObtainPairView.as_view()),
    path('jwt/refresh/', TokenRefreshView.as_view()),
    path('jwt/verify/', TokenVerifyView.as_view()),
]