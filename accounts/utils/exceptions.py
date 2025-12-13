from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    res = exception_handler(exc, context)
    if res is None:
        return None

    data = res.data
    if isinstance(data, dict) and "detail" in data:
        return res
    if isinstance(data, dict):
        res.data = {"detail": "Validation error", "errors": data}
        return res
    if isinstance(data, list):
        res.data = {"detail": "Validation error", "errors": {"non_field_errors": data}}
        return res
    return res
