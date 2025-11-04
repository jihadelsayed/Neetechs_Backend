from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter

from home.views import github_webhook
from Neetechs.api_router import (
    CategoryViewSet,
    ServicePostViewSet,
    ChatThreadViewSet,
    ProfileViewSet,
    HomeSliderViewSet,
    HomeContainersViewSet,
)
from Neetechs.views import api_index, healthz, legacy_redirect_view, readyz, root_view

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("services", ServicePostViewSet, basename="services")
router.register("chat", ChatThreadViewSet, basename="chat")
router.register("profile", ProfileViewSet, basename="profile")
router.register("home/slider", HomeSliderViewSet, basename="home-slider")
router.register("home/containers", HomeContainersViewSet, basename="home-containers")

api_v1_patterns = [
    path("", include((router.urls, "api-v1"), namespace="api-v1")),
    path("auth/", include(("Neetechs.urls_auth", "api-auth"), namespace="api-auth")),
    path("services/actions/", include(("Service.api.urls", "service_api"))),
    path("profile/", include("Profile.urls")),
    path("checkout/", include("Checkout.urls")),
    path("report/", include("report.urls")),
    path("trees/", include("trees.urls")),
]

urlpatterns = [
    path("", root_view, name="root"),
    path("admin/", admin.site.urls),
    path("healthz/", healthz, name="healthz"),
    path("readyz/", readyz, name="readyz"),
    path("api/", api_index, name="api-index"),
    path("api/v1/", include(api_v1_patterns)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("webhooks/github/", github_webhook, name="github-webhook"),
    path("service/", include(("Service.urls", "service"))),
    path("api/service/", include(("Service.api.urls", "service_api_legacy"))),
    path("api/categories/", include("Category.urls")),
    path("api/profile/", include("Profile.urls")),  # legacy deep paths
    path("api/chat/", include("chat.urls")),
    path("api/", include("Checkout.urls")),
    path("", include("knox_allauth.urls", namespace="knox_allauth")),
]

legacy_redirects = [
    ("auth/login/", "/api/v1/auth/login/", True),
    ("auth/register/", "/api/v1/auth/register/", True),
    ("auth/facebook/", "/api/v1/auth/oauth/facebook/", True),
    ("auth/google/", "/api/v1/auth/oauth/google/", True),
    ("auth/otp/send_phone_otp/", "/api/v1/auth/otp/send/", True),
    ("auth/otp/verify_phone_otp/", "/api/v1/auth/otp/verify/", True),
    ("set-password/", "/api/v1/auth/password/set/", True),
    ("api/categories/", "/api/v1/categories/", False),
    ("api/service/", "/api/v1/services/", False),
    ("api/chat/", "/api/v1/chat/", False),
    ("api/profile/", "/api/v1/profile/", False),
    ("api/home/list/HomeSlider", "/api/v1/home/slider/", False),
    ("api/home/list/HomeContainers", "/api/v1/home/containers/", False),
    ("github-webhook/", "/webhooks/github/", True),
]

for legacy_path, target, needs_post in legacy_redirects:
    code = 308 if needs_post else 301
    urlpatterns.append(path(legacy_path, legacy_redirect_view(target, status_code=code)))

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
