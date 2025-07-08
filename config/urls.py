from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from drf_spectacular.openapi import AutoSchema
from rest_framework import permissions
from config.settings import (
    base as settings,
    django_settings_module,
)


class BothHttpAndHttpsSchemaGenerator(AutoSchema):
    """Custom schema generator for HTTP/HTTPS handling"""

    def get_servers(self):
        if django_settings_module == "development":
            return [{"url": "http://localhost:8000/api/v1", "description": "Development server"}]
        else:
            return [{"url": "https://admin.77.uz/api/v1", "description": "Production server"}]


urlpatterns = [
    path("default-admin-panel/", admin.site.urls),

    # API endpoints
    path("api/v1/accounts/", include(("apps.accounts.urls", "accounts"), "accounts")),
    path("api/v1/store/", include(("apps.store.urls", "store"), "store")),
    path("api/v1/common/", include(("apps.common.urls", "common"), "common")),
]

if django_settings_module == "development":
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="schema-redoc",
        ),
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            SpectacularAPIView.as_view(),
            name="schema-json",
        ),
    ]
