from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.blog.urls', namespace='blog')),
    path('api/', include('api.blog_api.urls', namespace='blog_api'))
]
