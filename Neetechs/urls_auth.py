"""Versioned authentication endpoints."""
from django.urls import path
from dj_rest_auth.views import LogoutView

from knox_allauth.views_auth import (
    KnoxLoginView,
    KnoxRegisterView,
    FacebookLogin,
    GoogleLogin,
    EmailConfirmation,
    CurrentUserView,
)
from knox_allauth.views_otp import SendPhoneOTP, VerifyPhoneOTP
from knox_allauth.views_set_password import SetPasswordView

app_name = "auth"

urlpatterns = [
    path("login/", KnoxLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", KnoxRegisterView.as_view(), name="register"),
    path("password/set/", SetPasswordView.as_view(), name="password-set"),
    path("otp/send/", SendPhoneOTP.as_view(), name="otp-send"),
    path("otp/verify/", VerifyPhoneOTP.as_view(), name="otp-verify"),
    path("oauth/google/", GoogleLogin.as_view(), name="oauth-google"),
    path("oauth/facebook/", FacebookLogin.as_view(), name="oauth-facebook"),
    path("me/", CurrentUserView.as_view(), name="me"),
    path("email/resend/", EmailConfirmation.as_view(), name="email-resend"),
]
