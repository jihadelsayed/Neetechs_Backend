from knox.models import AuthToken
from rest_framework.views import exception_handler


def create_knox_token(token_model, user, serializer):
    """
    Compatibility hook used by dj-rest-auth/knox integration.
    Signature stays as-is, but we intentionally ignore token_model/serializer.
    """
    _, token = AuthToken.objects.create(user)
    return token


def custom_exception_handler(exc, context):
    res = exception_handler(exc, context)
    if res is None:
        return None

    data = res.data

    # If it's already the shape we want, keep it.
    if isinstance(data, dict) and "detail" in data:
        return res

    # Normalize DRF validation errors into:
    # {"detail": "Validation error", "errors": {...}}
    if isinstance(data, dict):
        res.data = {"detail": "Validation error", "errors": data}
        return res

    # Sometimes DRF returns a list for non-field errors
    if isinstance(data, list):
        res.data = {"detail": "Validation error", "errors": {"non_field_errors": data}}
        return res

    return res
