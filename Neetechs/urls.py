from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from Neetechs.views import root_view, healthz, readyz

urlpatterns = [
    # Root
    path("", root_view, name="root"),

    # Admin & health
    path("admin/", admin.site.urls),
    path("healthz/", healthz, name="healthz"),
    path("readyz/", readyz, name="readyz"),

    # API v1 (single public surface)
    path("api/v1/accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("api/v1/payments/", include(("payments.urls", "payments"), namespace="payments")),
    path("api/v1/checkout/", include(("Checkout.urls", "checkout"), namespace="checkout")),

    # Digital products (kept non-versioned as you requested)
    path("digital-products/", include(("DigitalProduct.urls", "digital-products"), namespace="digital-products")),

    # API docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
