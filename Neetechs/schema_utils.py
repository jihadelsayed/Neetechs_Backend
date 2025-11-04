"""
Shared schema helper utilities for drf-spectacular customisations.
"""
from drf_spectacular.utils import (
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    extend_schema_field,
)


def schema_response_ok(obj_schema):
    """Return a 200 response mapping for simple success payloads."""
    return {200: OpenApiResponse(obj_schema)}


def schema_ack():
    """Return a simple 200 acknowledgement response without a payload."""
    return {200: OpenApiResponse(description="OK")}


def no_body():
    """Decorator to document endpoints that do not accept a request body."""
    return extend_schema(request=None, responses=schema_ack())
