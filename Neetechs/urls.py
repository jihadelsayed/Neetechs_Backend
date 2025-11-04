from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from home.views import github_webhook
from Neetechs.api_router import (
    CategoryViewSet,
    ChatThreadViewSet,
    HomeContainersViewSet,
    HomeSliderViewSet,
    ProfileViewSet,
    ServicePostViewSet,
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
    path("services/", include(("Service.api.urls", "services"))),
    path("profile/", include(("Profile.urls", "profile"))),
    path("checkout/", include(("Checkout.urls", "checkout"))),
    path("report/", include(("report.urls", "report"))),
    path("trees/", include(("trees.urls", "trees"))),
    path("chat/", include(("chat.urls", "chat"))),
    path("home/", include(("home.urls", "home"))),
    path("", include((router.urls, "api-v1"), namespace="api-v1")),
    path("auth/", include(("Neetechs.urls_auth", "api-auth"), namespace="api-auth")),
    path("services/", include(("Service.api.urls", "service_api"))),
    path("profile/", include("Profile.urls")),
    path("chat/", include("chat.urls")),
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
    path("", include("knox_allauth.urls", namespace="knox_allauth")),
]

legacy_redirect_patterns = [
    # Auth migrations
    path("auth/login/", legacy_redirect_view("/api/v1/auth/login/", status_code=308)),
    path("auth/logout/", legacy_redirect_view("/api/v1/auth/logout/", status_code=308)),
    path("auth/register/", legacy_redirect_view("/api/v1/auth/register/", status_code=308)),
    path("auth/user/", legacy_redirect_view("/api/v1/auth/me/", status_code=308)),
    path("auth/otp/send/", legacy_redirect_view("/api/v1/auth/otp/send/", status_code=308)),
    path("auth/otp/verify/", legacy_redirect_view("/api/v1/auth/otp/verify/", status_code=308)),
    path("auth/facebook/", legacy_redirect_view("/api/v1/auth/oauth/facebook/", status_code=308)),
    path("auth/google/", legacy_redirect_view("/api/v1/auth/oauth/google/", status_code=308)),
    path("auth/password/change/", legacy_redirect_view("/api/v1/auth/password/set/", status_code=308)),
    path("auth/password/reset/", legacy_redirect_view("/api/v1/auth/password/set/", status_code=308)),
    path("auth/password/reset/confirm/", legacy_redirect_view("/api/v1/auth/password/set/", status_code=308)),
    path("verify-email/again/", legacy_redirect_view("/api/v1/auth/email/resend/", status_code=308)),

    # Service API migrations
    path("api/service/", legacy_redirect_view("/api/v1/services/", status_code=308)),
    path("api/service/list/", legacy_redirect_view("/api/v1/services/", status_code=308)),
    path("api/service/create/", legacy_redirect_view("/api/v1/services/", status_code=308)),
    path("api/service/<slug:slug>/", legacy_redirect_view("/api/v1/services/{slug}/", status_code=308)),
    path("api/service/<slug:slug>/update/", legacy_redirect_view("/api/v1/services/{slug}/", status_code=308)),
    path("api/service/<slug:slug>/delete/", legacy_redirect_view("/api/v1/services/{slug}/", status_code=308)),
    path("api/service/<slug:slug>/is_employee/", legacy_redirect_view("/api/v1/services/{slug}/is-employee/", status_code=308)),
    path("api/service/Category/", legacy_redirect_view("/api/v1/services/filters/category/", status_code=308)),
    path("api/service/SubCategory/", legacy_redirect_view("/api/v1/services/filters/sub_category/", status_code=308)),
    path("api/service/Country/", legacy_redirect_view("/api/v1/services/filters/country/", status_code=308)),
    path("api/service/State/", legacy_redirect_view("/api/v1/services/filters/state/", status_code=308)),
    path("api/service/City/", legacy_redirect_view("/api/v1/services/filters/city/", status_code=308)),
    path("api/service/Comments/", legacy_redirect_view("/api/v1/services/filters/comments/", status_code=308)),
    path("api/service/Likes/", legacy_redirect_view("/api/v1/services/filters/likes/", status_code=308)),
    path("api/service/DisLikes/", legacy_redirect_view("/api/v1/services/filters/dislikes/", status_code=308)),
    path("api/service/filter/", legacy_redirect_view("/api/v1/services/search/", status_code=308)),
    path("api/service/list", legacy_redirect_view("/api/v1/services/", status_code=308)),
    path("api/service/create", legacy_redirect_view("/api/v1/services/", status_code=308)),
    path("api/service/<slug:slug>", legacy_redirect_view("/api/v1/services/{slug}/", status_code=308)),
    path("api/service/<slug:slug>/update", legacy_redirect_view("/api/v1/services/{slug}/", status_code=308)),
    path("api/service/<slug:slug>/delete", legacy_redirect_view("/api/v1/services/{slug}/", status_code=308)),
    path("api/service/<slug:slug>/is_employee", legacy_redirect_view("/api/v1/services/{slug}/is-employee/", status_code=308)),

    # Category + chat + home
    path("api/categories/", legacy_redirect_view("/api/v1/categories/", status_code=308)),
    path("api/categories/<str:name>/", legacy_redirect_view("/api/v1/categories/{name}/", status_code=308)),
    path("api/categories/<str:name>", legacy_redirect_view("/api/v1/categories/{name}/", status_code=308)),
    re_path(r"^api/chat/(?P<rest>.*)$", legacy_redirect_view("/api/v1/chat/{rest}", status_code=308)),
    path("api/home/list/HomeSlider", legacy_redirect_view("/api/v1/home/slider/", status_code=308)),
    path("api/home/list/HomeContainers", legacy_redirect_view("/api/v1/home/containers/", status_code=308)),

    # Checkout & webhooks
    re_path(r"^api/webhook/?$", legacy_redirect_view("/api/v1/checkout/webhook", status_code=308)),
    path("github-webhook/", legacy_redirect_view("/webhooks/github/", status_code=308)),

    # Profile clean-up
    path("api/v1/profile/profile/<str:site_id>/", legacy_redirect_view("/api/v1/profile/{site_id}/", status_code=308)),
    path("api/v1/profile/profile/<str:site_id>", legacy_redirect_view("/api/v1/profile/{site_id}/", status_code=308)),
    path("api/v1/profile/profile/allprofileinfo/<str:site_id>/", legacy_redirect_view("/api/v1/profile/all/{site_id}/", status_code=308)),
    path("api/v1/profile/profile/allprofileinfo/<str:site_id>", legacy_redirect_view("/api/v1/profile/all/{site_id}/", status_code=308)),
    path("api/v1/profile/profile/list/Kompetenser_intygs", legacy_redirect_view("/api/v1/profile/certifications/", status_code=308)),
    path("api/v1/profile/profile/post/Kompetenser_intygs", legacy_redirect_view("/api/v1/profile/certifications/create/", status_code=308)),
    path("api/v1/profile/profile/Kompetenser_intyg/<int:id>/", legacy_redirect_view("/api/v1/profile/certifications/{id}/", status_code=308)),
    path("api/v1/profile/profile/Kompetenser_intyg/<int:id>", legacy_redirect_view("/api/v1/profile/certifications/{id}/", status_code=308)),
    path("api/v1/profile/profile/list/Intressens", legacy_redirect_view("/api/v1/profile/interests/", status_code=308)),
    path("api/v1/profile/profile/post/Intressens", legacy_redirect_view("/api/v1/profile/interests/create/", status_code=308)),
    path("api/v1/profile/profile/Intressen/<int:id>/", legacy_redirect_view("/api/v1/profile/interests/{id}/", status_code=308)),
    path("api/v1/profile/profile/Intressen/<int:id>", legacy_redirect_view("/api/v1/profile/interests/{id}/", status_code=308)),
    path("api/v1/profile/profile/list/Studiers", legacy_redirect_view("/api/v1/profile/studies/", status_code=308)),
    path("api/v1/profile/profile/post/Studiers", legacy_redirect_view("/api/v1/profile/studies/create/", status_code=308)),
    path("api/v1/profile/profile/Studier/<int:id>/", legacy_redirect_view("/api/v1/profile/studies/{id}/", status_code=308)),
    path("api/v1/profile/profile/Studier/<int:id>", legacy_redirect_view("/api/v1/profile/studies/{id}/", status_code=308)),
    path("api/v1/profile/profile/list/Erfarenhets", legacy_redirect_view("/api/v1/profile/experience/", status_code=308)),
    path("api/v1/profile/profile/post/Erfarenhets", legacy_redirect_view("/api/v1/profile/experience/create/", status_code=308)),
    path("api/v1/profile/profile/Erfarenhet/<int:id>/", legacy_redirect_view("/api/v1/profile/experience/{id}/", status_code=308)),
    path("api/v1/profile/profile/Erfarenhet/<int:id>", legacy_redirect_view("/api/v1/profile/experience/{id}/", status_code=308)),
]

urlpatterns += legacy_redirect_patterns

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
