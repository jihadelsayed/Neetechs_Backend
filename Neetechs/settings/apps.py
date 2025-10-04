INSTALLED_APPS = [
    # Django
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    # Third-party
    "corsheaders",
    "rest_framework","rest_framework.authtoken","drf_spectacular","django_filters",
    "channels","knox",
    "allauth","allauth.account","allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.twitter",
    "fcm_django",
    # Your apps
    "chat","Profile","Service","Checkout","home","report","Category","knox_allauth","stripe",
]
