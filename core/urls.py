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
    # path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/v1/oauth2/', include('apps.social_auth.urls')),
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/', include('apps.anidb.urls', namespace='animes')),
    # path('api/v1/', include('apps.blog.urls', namespace='posts')),

    # swagger documentating
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
