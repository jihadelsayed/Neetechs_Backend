from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views_auth import (
    KnoxLoginView,
    KnoxRegisterView,
    FacebookLogin,
    GoogleLogin,
    EmailConfirmation,
)
from .views_otp import SendPhoneOTP, VerifyPhoneOTP
from .views_set_password import SetPasswordView
from .webauthn_view import (
    begin_registration,
    complete_registration,
    begin_authentication,
    complete_authentication,
)

app_name = "accounts"

urlpatterns = [
    path("auth/login/", KnoxLoginView.as_view(), name="login"),
    path("auth/register/", KnoxRegisterView.as_view(), name="register"),
    path("auth/facebook/", FacebookLogin.as_view(), name="fb_login"),
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),

    path("auth/", include("dj_rest_auth.urls")),
    path("accounts/", include("allauth.urls")),

    path("verify-email/again/", EmailConfirmation.as_view(), name="resend_email_confirmation"),

    path("auth/otp/send/", SendPhoneOTP.as_view(), name="send_phone_otp"),
    path("auth/otp/verify/", VerifyPhoneOTP.as_view(), name="verify_phone_otp"),

    path("auth/webauthn/begin-registration/", begin_registration, name="webauthn_begin_registration"),
    path("auth/webauthn/finish-registration/", complete_registration, name="webauthn_finish_registration"),
    path("auth/webauthn/begin-login/", begin_authentication, name="webauthn_begin_login"),
    path("auth/webauthn/finish-login/", complete_authentication, name="webauthn_finish_login"),

    path("set-password/", SetPasswordView.as_view(), name="set_password"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
