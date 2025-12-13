import stripe

from django.conf import settings
from django.db import transaction

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from dj_rest_auth.registration.views import RegisterView
from allauth.account import app_settings as allauth_settings
from allauth.account.utils import complete_signup

from accounts.serializers import AuthResponseSerializer, PublicUserSerializer
from accounts.throttles import RegisterThrottle
from ...utils.knox import create_knox_token
from ...serializers.register import RegisterRequestSerializer
from drf_spectacular.utils import extend_schema


def _stripe_customer_create(email: str):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe.Customer.create(email=email)


def _stable_placeholder_email(*, email: str | None, phone: str | None) -> str:
    email = (email or "").strip()
    phone = (phone or "").strip()
    if email:
        return email
    if phone:
        return f"no-email-{phone}@phone.neetechs.invalid"
    return "no-email-anonymous@neetechs.invalid"


@extend_schema(
    request=RegisterRequestSerializer,
    responses={200: AuthResponseSerializer},
    tags=["accounts-auth"],
)
class KnoxRegisterView(RegisterView):
    permission_classes = [AllowAny]
    serializer_class = RegisterRequestSerializer
    throttle_classes = [RegisterThrottle]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()  # ✅ correct

        token = create_knox_token(user)  # ✅ user-only helper

        req_email = request.data.get("email")
        req_phone = request.data.get("phone")
        customer_email = _stable_placeholder_email(email=req_email, phone=req_phone)

        def _after_commit():
            try:
                customer = _stripe_customer_create(customer_email)
            except Exception:
                return
            type(user).objects.filter(pk=user.pk, stripe_customer_id__isnull=True).update(
                stripe_customer_id=customer.id
            )

        transaction.on_commit(_after_commit)

        complete_signup(
            request._request,
            user,
            allauth_settings.EMAIL_VERIFICATION,
            None,
            signal_kwargs={"sociallogin": None},
        )

        return Response(
            {"token": token, "user": PublicUserSerializer(user).data},
            status=status.HTTP_200_OK,
        )
