# Neetechs/settings/prod.py
# Production settings simply re-use everything from the package __init__

from . import *  # noqa
# USE_X_FORWARDED_HOST = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CACHES = {
  "default": {
    "BACKEND": "django_redis.cache.RedisCache",
    "LOCATION": "redis://127.0.0.1:6379/1",
    "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
  }
}
