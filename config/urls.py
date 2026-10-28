from django.contrib import admin
from django.urls import path, include
from products.auth_views import CustomObtainAuthToken
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from products.auth_views import (
    RegisterAPIView,
    CustomObtainAuthToken,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/register/", RegisterAPIView.as_view(), name="api-register"),
    path("api/token/", CustomObtainAuthToken.as_view(), name="api_token_auth",),
    path("api/", include("products.urls")),
    path("", include("frontend.urls")),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
