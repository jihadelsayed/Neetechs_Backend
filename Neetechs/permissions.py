"""
Project-wide DRF permission helpers.
"""
import hashlib
import hmac
import secrets

from django.conf import settings
from rest_framework.permissions import BasePermission, SAFE_METHODS

import stripe


class ReadOnlyOrStaff(BasePermission):
    """
    Allow safe methods for everyone, but limit write access to staff members.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = getattr(request, "user", None)
        return bool(user and user.is_staff)


class DeployWebhookPermission(BasePermission):
    """
    Allow webhook POSTs that provide the expected deployment secret header.

    Supports either the legacy ``X-DEPLOY-SECRET`` header or GitHub's
    ``X-Hub-Signature-256`` HMAC signature.
    """

    message = "Missing or invalid deployment secret."
    legacy_header = "X-DEPLOY-SECRET"
    github_signature_header = "X-Hub-Signature-256"

    def has_permission(self, request, view):
        secret = getattr(settings, "GITHUB_WEBHOOK_SECRET", "")
        if not secret:
            return False

        signature = request.headers.get(self.github_signature_header)
        if signature:
            return self._valid_github_signature(signature, request, secret)

        provided = request.headers.get(self.legacy_header, "")
        return bool(provided) and secrets.compare_digest(provided, secret)

    def _valid_github_signature(self, header_value, request, secret):
        if not header_value.startswith("sha256="):
            return False

        provided = header_value.split("=", 1)[1]
        digest = hmac.new(
            secret.encode("utf-8"),
            msg=request.body or b"",
            digestmod=hashlib.sha256,
        ).hexdigest()

        if not secrets.compare_digest(provided, digest):
            return False

        setattr(request, "_github_signature_validated", True)
        setattr(request, "_github_event", request.headers.get("X-GitHub-Event"))
        setattr(request, "_github_delivery", request.headers.get("X-GitHub-Delivery"))
        return True


class StripeWebhookPermission(BasePermission):
    """
    Validate incoming Stripe webhook signatures before DRF dispatches the view.
    """

    message = "Invalid Stripe webhook signature."

    def has_permission(self, request, view):
        secret = getattr(settings, "STRIPE_WEBHOOK_SECRET", "")
        if not secret:
            return False

        signature = request.headers.get("stripe-signature")
        if not signature:
            return False

        try:
            event = stripe.Webhook.construct_event(
                payload=request.body, sig_header=signature, secret=secret
            )
        except Exception:
            return False

        # Cache the event on the request so the view can reuse the verified payload.
        setattr(request, "_stripe_event", event)
        return True
