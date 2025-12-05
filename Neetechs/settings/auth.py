# settings/auth.py
# settings/auth.py
ACCOUNT_EMAIL_VERIFICATION = "optional"

# allow both email & username at login
ACCOUNT_LOGIN_METHODS = {"email", "username"}

# star = required; username is optional here
ACCOUNT_SIGNUP_FIELDS = ["username*", "email", "password1*", "password2*"]

DJ_REST_AUTH = {
    "SIGNUP_FIELDS": {
        "username":  {"required": True},
        "email":     {"required": False},   # optional because phone is allowed
        "password1": {"required": True},
        "password2": {"required": True},
        "phone":     {"required": False},
    },
    "REGISTER_SERIALIZER": "accounts.serializers.RegisterWithPhoneSerializer",
}

AUTHENTICATION_BACKENDS = [
    "accounts.backends.EmailOrPhoneBackend",  # handles email, username, phone
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
