import stripe
from django.conf import settings

from rest_framework.permissions import AllowAny

from dj_rest_auth.registration.views import RegisterView
from allauth.account import app_settings as allauth_settings
from allauth.account.utils import complete_signup

from ...utils import create_knox_token
from ...serializers.register import PhoneOrEmailRegisterSerializer


def _stripe_customer_create(email: str):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe.Customer.create(email=email)


class KnoxRegisterView(RegisterView):
    permission_classes = [AllowAny]
    serializer_class = PhoneOrEmailRegisterSerializer

    def perform_create(self, serializer):
        phone_number = self.request.data.get("phone")
        customer_email = self.request.data.get("email") or (
            f"no-email-{phone_number}@neetechs.com"
            if phone_number
            else f"no-email-anonymous@{getattr(settings,'DEFAULT_DOMAIN','neetechs.com')}"
        )

        customer = _stripe_customer_create(customer_email)
        user = serializer.save(self.request)

        user.stripe_customer_id = customer.id
        user.save(update_fields=["stripe_customer_id"])

        token = create_knox_token(None, user, None)

        complete_signup(
            self.request._request,
            user,
            allauth_settings.EMAIL_VERIFICATION,
            None,
            signal_kwargs={"sociallogin": None},
        )

        self.token = (None, token)
        return user
