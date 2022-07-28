from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .tokens import MyTokenObtainPairView

app_name = 'oauth2'

urlpatterns = [
    # path('', auth_views.google_login, name='google-login'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]