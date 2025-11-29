from django.urls import path
from .views import (
    stripe_webhook,
    create_checkout_session,
    create_bundle_checkout_session,
)

urlpatterns = [
    path("webhook/", stripe_webhook, name="stripe-webhook"),
    path("checkout/digital-product/", create_checkout_session),
    path("checkout/bundle/", create_bundle_checkout_session),
]
