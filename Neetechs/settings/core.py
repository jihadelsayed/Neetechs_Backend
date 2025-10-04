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
AUTH_USER_MODEL = "knox_allauth.CustomUser"

ROOT_URLCONF = "Neetechs.urls"
WSGI_APPLICATION = "Neetechs.wsgi.application"
ASGI_APPLICATION = "Neetechs.asgi.application"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media_cdn"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
