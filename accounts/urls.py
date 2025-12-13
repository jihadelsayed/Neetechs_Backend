from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views_auth import KnoxLoginView, KnoxRegisterView, FacebookLogin, GoogleLogin, EmailConfirmation
from .views_otp import SendPhoneOTP, VerifyPhoneOTP
from .views_set_password import SetPasswordView
from .webauthn_view import begin_registration, complete_registration, begin_authentication, complete_authentication
from .views_profile import SetHandleView

app_name = "accounts"

urlpatterns = [
    # auth (email/password + social)
    path("auth/login/", KnoxLoginView.as_view(), name="auth_login"),
    path("auth/register/", KnoxRegisterView.as_view(), name="auth_register"),
    path("auth/social/facebook/", FacebookLogin.as_view(), name="auth_facebook"),
    path("auth/social/google/", GoogleLogin.as_view(), name="auth_google"),

    # dj-rest-auth + allauth
    path("auth/", include("dj_rest_auth.urls")),
    path("accounts/", include("allauth.urls")),

    # email verify (resend)
    path("auth/email/resend/", EmailConfirmation.as_view(), name="auth_email_resend"),

    # otp
    path("auth/otp/send/", SendPhoneOTP.as_view(), name="auth_otp_send"),
    path("auth/otp/verify/", VerifyPhoneOTP.as_view(), name="auth_otp_verify"),

    # webauthn (passkeys)
    path("auth/webauthn/register/begin/", begin_registration, name="webauthn_register_begin"),
    path("auth/webauthn/register/finish/", complete_registration, name="webauthn_register_finish"),
    path("auth/webauthn/login/begin/", begin_authentication, name="webauthn_login_begin"),
    path("auth/webauthn/login/finish/", complete_authentication, name="webauthn_login_finish"),

    # set password (after OTP login)
    path("auth/password/set/", SetPasswordView.as_view(), name="auth_password_set"),
    
    path("me/handle/", SetHandleView.as_view(), name="me_handle"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
