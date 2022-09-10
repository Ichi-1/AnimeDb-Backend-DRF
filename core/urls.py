from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

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
    # path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),


    # Spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


    path('api/auth/', include('apps.authentication.urls', namespace='auth')),
    path('api/users/', include('apps.users.urls', namespace='users')),
    #
    path('api/', include('apps.anime_db.urls', namespace='anime_db')),
    path('api/', include('apps.manga_db.urls', namespace='manga_db')),
    path('api/', include('apps.activity.urls', namespace='activity')),
]
