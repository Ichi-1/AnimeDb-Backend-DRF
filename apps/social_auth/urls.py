from django.urls import path

from .views import GoogleLoginAPIView

app_name = 'oauth2'

urlpatterns = [
    path('google/', GoogleLoginAPIView.as_view())
]
