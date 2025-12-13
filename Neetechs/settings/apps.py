INSTALLED_APPS = [
    # Django
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
   "django.contrib.sites", # Third-party
    "corsheaders",
    "storages",
     #"dj_rest_auth",
 
    #"imagekit",
    "payments",
 
    "accounts.apps.AccountsConfig",

    "rest_framework","rest_framework.authtoken","drf_spectacular","django_filters",
    "channels","knox",
    "allauth","allauth.account","allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.twitter",
    "fcm_django",
    # Your apps
    "chat","Profile","DigitalProduct","product","Service","Checkout","home","report","Category","accounts","trees",
]
