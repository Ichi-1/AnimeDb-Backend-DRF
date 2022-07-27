from django.urls import path
from django.views.generic import TemplateView

app_name = 'blog'

urlpatterns = [
    path('api/post', TemplateView.as_view(template_name='index.html'))
]