
from knox.models import AuthToken

from rest_framework.views import exception_handler

def create_knox_token(token_model, user, serializer):
    _, token = AuthToken.objects.create(user)
    return token

def custom_exception_handler(exc, context):
    res = exception_handler(exc, context)
    if res is None:
        return res

    # Normalize into {"detail": "...", "errors": {...}}
    if isinstance(res.data, dict):
        if "detail" in res.data:
            return res
        return res.__class__({"detail": "Validation error", "errors": res.data}, status=res.status_code)

    return res