"""Neetechs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('service/', include('service.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

#from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

#from personal.views import (
#	home_screen_view,
#)

urlpatterns = [
    #path("", lambda request: JsonResponse({"status": "Neetechs API is running"})),

    path('admin/', admin.site.urls),
  #  path('', include('Service.urls')),
    path('', include('knox_allauth.url')),
    path('service/', include('Service.urls', 'service')),
    path('categories/', include('Category.urls')),
    path('api/service/', include('Service.api.urls', 'service_api')),
    path('', include('chat.urls')),
    path('', include('Profile.urls')),
    path('', include('home.urls')),
    path('', include('report.urls')),
    path('', include('Checkout.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),


    #path('devices', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),

    
    #path("stripe/", include("djstripe.urls", namespace="djstripe")), #add this



   # path('', home_screen_view, name="home"),
#    path('account/', account_view, name="account"),
#    path('login/', login_view, name="login"),
#    path('logout/', logout_view, name="logout"),
#    path('must_authenticate/', must_authenticate_view, name="must_authenticate"),
#    path('register/', registration_view, name="register"),
	
	# REST-framework
#    path('api/account/', include('account.api.urls', 'account_api')),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
#    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
 #       name='password_change_done'),
#
#    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
 #       name='password_change'),

  #  path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
   #  name='password_reset_done'),

#    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
 #   path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
  #  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
   #  name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)