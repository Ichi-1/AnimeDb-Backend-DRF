from django.urls import path

from .views import GoogleLoginAPIView, GitHubLoginAPIView

app_name = 'oauth2'

urlpatterns = [
    path('google/', GoogleLoginAPIView.as_view()),
    path('github/', GitHubLoginAPIView.as_view()),
]
