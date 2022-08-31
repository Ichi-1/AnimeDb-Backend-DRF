from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="MyAniDB API",
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

    path('api/v1/', include('apps.anime_db.urls', namespace='anime_db')),
    path('api/v1/auth/', include('apps.authentication.urls', namespace='auth')),
    path('api/v1/users/', include('apps.users.urls', namespace='users')),

    # swagger documentating
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
