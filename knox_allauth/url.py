from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import EmailConfirmation, KnoxLoginView, KnoxRegisterView, FacebookLogin, GoogleLogin

urlpatterns = [ 
	path('auth/login/', KnoxLoginView.as_view()),
	path('auth/register/', KnoxRegisterView.as_view()),
	path('auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
	path('auth/google/', GoogleLogin.as_view(), name='google_login'),
	path('auth/', include('dj_rest_auth.urls')),
	path('accounts/', include('allauth.urls')),
	path('verify-email/again/', EmailConfirmation.as_view(), name='resend-email-confirmation'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
