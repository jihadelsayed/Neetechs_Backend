from django.conf import settings
from django.urls import path

from .views.otp import SendPhoneOTP, VerifyPhoneOTP
from .views.set_password import SetPasswordView
from .views.profile import SetHandleView
from .views.me import MeView

from .views.auth import (
    KnoxLoginView,
    KnoxRegisterView,
    FacebookLogin,
    GoogleLogin,
    EmailConfirmation,
)

app_name = "accounts"

urlpatterns = [
    # Auth (email/password + social)
    path("auth/login/", KnoxLoginView.as_view(), name="auth_login"),
    path("auth/register/", KnoxRegisterView.as_view(), name="auth_register"),
    path("auth/social/facebook/", FacebookLogin.as_view(), name="auth_facebook"),
    path("auth/social/google/", GoogleLogin.as_view(), name="auth_google"),

    # Email verify (resend)
    path("auth/email/resend/", EmailConfirmation.as_view(), name="auth_email_resend"),

    # OTP
    path("auth/otp/send/", SendPhoneOTP.as_view(), name="auth_otp_send"),
    path("auth/otp/verify/", VerifyPhoneOTP.as_view(), name="auth_otp_verify"),

    # Set password (after OTP login)
    path("auth/password/set/", SetPasswordView.as_view(), name="auth_password_set"),

    # Current user
    path("me/", MeView.as_view(), name="me"),
    path("me/handle/", SetHandleView.as_view(), name="me_handle"),
]

# WebAuthn (passkeys) — gated so it can’t accidentally be exposed in prod
if getattr(settings, "WEBAUTHN_ENABLED", False):
    from .views.webauthn import (
        begin_registration,
        complete_registration,
        begin_authentication,
        complete_authentication,
    )

    urlpatterns += [
        path("auth/webauthn/register/begin/", begin_registration, name="webauthn_register_begin"),
        path("auth/webauthn/register/finish/", complete_registration, name="webauthn_register_finish"),
        path("auth/webauthn/login/begin/", begin_authentication, name="webauthn_login_begin"),
        path("auth/webauthn/login/finish/", complete_authentication, name="webauthn_login_finish"),
    ]
