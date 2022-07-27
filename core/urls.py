from django.contrib import admin
from django.urls import include, path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    # api namespasec
    path('', include('api.anidb_api.urls', namespace='anime-api')),
    path('', include('api.blog_api.urls', namespace='blog-api')),
    path('', include('apps.oauth.urls', namespace='oauth-api')),

    # swagger documentating
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
