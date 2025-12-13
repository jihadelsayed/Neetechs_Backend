import stripe

from django.conf import settings
from django.db import transaction

from rest_framework.permissions import AllowAny

from dj_rest_auth.registration.views import RegisterView
from allauth.account import app_settings as allauth_settings
from allauth.account.utils import complete_signup

from accounts.serializers import AuthResponseSerializer

from ...utils.knox import create_knox_token
from ...serializers.register import RegisterRequestSerializer
from drf_spectacular.utils import extend_schema


def _stripe_customer_create(email: str):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe.Customer.create(email=email)


def _stable_placeholder_email(*, email: str | None, phone: str | None) -> str:
    """
    Keep placeholder emails consistent and safe.
    - If email provided, use it.
    - If phone-only, use a stable invalid domain.
    """
    email = (email or "").strip()
    phone = (phone or "").strip()

    if email:
        return email

    if phone:
        # stable but not leaking real domains; domain intentionally invalid
        return f"no-email-{phone}@phone.neetechs.invalid"

    return f"no-email-anonymous@neetechs.invalid"


@extend_schema(
    request=RegisterRequestSerializer,
    responses={200: AuthResponseSerializer},
    tags=["accounts-auth"],
)
class KnoxRegisterView(RegisterView):
    permission_classes = [AllowAny]
    serializer_class = RegisterRequestSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        # 1) Create user FIRST (inside transaction)
        user = serializer.save(self.request)

        # 2) Create token now (pure DB / local)
        token = create_knox_token(None, user, None)

        # 3) Schedule Stripe creation AFTER the user commit succeeds
        req_email = self.request.data.get("email")
        req_phone = self.request.data.get("phone")
        customer_email = _stable_placeholder_email(email=req_email, phone=req_phone)

        def _after_commit():
            try:
                customer = _stripe_customer_create(customer_email)
            except Exception:
                # Stripe failure should not break registration.
                # User can be repaired later or via a background job.
                return

            # update only the stripe field (outside the transaction is fine)
            type(user).objects.filter(pk=user.pk, stripe_customer_id__isnull=True).update(
                stripe_customer_id=customer.id
            )

        transaction.on_commit(_after_commit)

        # 4) Allauth signup flow (kept)
        complete_signup(
            self.request._request,
            user,
            allauth_settings.EMAIL_VERIFICATION,
            None,
            signal_kwargs={"sociallogin": None},
        )

        # 5) dj-rest-auth expects self.token like (None, token_string)
        self.token = (None, token)
        return user
