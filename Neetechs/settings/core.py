"""Neetechs.settings.core"""

from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parents[2]

def csv_env(key, default=""):
    raw = config(key, default=default)
    return [s.strip() for s in raw.split(",") if s.strip()]

def bool_env(key, default=False):
    return config(key, cast=bool, default=default)

SECRET_KEY = config("SECRET_KEY")
DEBUG = bool_env("DEBUG", False)

ALLOWED_HOSTS = csv_env("ALLOWED_HOSTS", "")
CSRF_TRUSTED_ORIGINS = csv_env("CSRF_TRUSTED_ORIGINS", "")
AUTH_USER_MODEL = "accounts.User"

ROOT_URLCONF = "Neetechs.urls"
WSGI_APPLICATION = "Neetechs.wsgi.application"
ASGI_APPLICATION = "Neetechs.asgi.application"
STATIC_URL = f"https://neetechs-static.s3.us-east-1.amazonaws.com/"

STATIC_ROOT = BASE_DIR / "staticfiles"  # harmless, even with S3
STATICFILES_DIRS = [
    BASE_DIR / "static"  # only if your project has /static/
]

# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"
# STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media_cdn"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
FRONTEND_SUCCESS_URL = config("FRONTEND_SUCCESS_URL")
FRONTEND_CANCEL_URL = config("FRONTEND_CANCEL_URL")
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = config("STRIPE_WEBHOOK_SECRET")
SITE_ID = 1
