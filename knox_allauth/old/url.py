from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from knox_allauth.views_otp import SendPhoneOTP, VerifyPhoneOTP
from knox_allauth.views_set_password import SetPasswordView

from .views import EmailConfirmation, KnoxLoginView, KnoxRegisterView, FacebookLogin, GoogleLogin
from .webauthn_view import (
    begin_registration,
    complete_registration,
    begin_authentication,
    complete_authentication,
)


urlpatterns = [ 
	path('auth/login/', KnoxLoginView.as_view()),
	path('auth/register/', KnoxRegisterView.as_view()),
	path('auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
	path('auth/google/', GoogleLogin.as_view(), name='google_login'),
	path('auth/', include('dj_rest_auth.urls')),
	path('accounts/', include('allauth.urls')),
	path('verify-email/again/', EmailConfirmation.as_view(), name='resend-email-confirmation'),
    
	
    path('auth/otp/send/', SendPhoneOTP.as_view()),
        path("auth/otp/verify/", VerifyPhoneOTP.as_view(), name="verify-phone-otp"),
        
    path("auth/webauthn/begin-registration/", begin_registration),
    path("auth/webauthn/finish-registration/", complete_registration),
    path("auth/webauthn/begin-login/", begin_authentication),
    path("auth/webauthn/finish-login/", complete_authentication),
    
    path('set-password/', SetPasswordView.as_view(), name='set-password'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
