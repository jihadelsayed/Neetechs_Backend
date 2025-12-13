from datetime import timedelta

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("knox.auth.TokenAuthentication",),
    
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticatedOrReadOnly",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 17,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "accounts.utils.exceptions.custom_exception_handler",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
        "otp": "3/min",       # ✅ matches OTPThrottle.scope = "otp"
        "login": "10/min",
        "register": "5/min",
    },

}
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"].update({
  "login": "10/min",
  "register": "5/min",
  "otp": "3/min",
})

REST_KNOX = {"TOKEN_TTL": timedelta(hours=100)}

SPECTACULAR_SETTINGS = {
    "TITLE": "Neetechs API",
    "DESCRIPTION": "OpenAPI for Neetechs Platform",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
