from django.contrib import admin
from django.urls import include, path
from rest_framework.reverse import reverse
from rest_framework import views, response
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)
from drf_spectacular.utils import extend_schema


class DocsView(views.APIView):
    """
    Rest Overview endpoint
    """
    @extend_schema(summary="Get Api Docs overview", description="Api Root")
    def get(self, request, *args, **kwargs):
        api_overview = {
            "swagger_ui": reverse("swagger-ui", request=request),
            "redoc": reverse("redoc", request=request)
        }
        return response.Response(api_overview)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("activity/", include('actstream.urls')),
    # path("root/", DocsView.as_view()),
    # Spectacular
    path("api/schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # my api
    path("api/auth/", include("apps.authentication.urls", namespace="auth")),
    path("api/", include("apps.users.urls", namespace="users")),
    #
    path("api/", include("apps.anime_db.urls")),
    path("api/", include("apps.manga_db.urls")),
    path("api/", include("apps.activity.urls")),
]
