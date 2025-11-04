"""Project-level utility views (health checks, API index, redirects)."""
from urllib.parse import urlencode

from django.http import HttpResponsePermanentRedirect, JsonResponse


def root_view(_request):
    return JsonResponse({"message": "Neetechs API", "docs": "/api/docs/"})


def healthz(_request):
    return JsonResponse({"status": "ok"})


def readyz(_request):
    return JsonResponse({"status": "ok"})


def api_index(_request):
    return JsonResponse(
        {
            "versions": {
                "v1": {
                    "base": "/api/v1/",
                    "docs": "/api/docs/",
                    "resources": [
                        "/api/v1/categories/",
                        "/api/v1/services/",
                        "/api/v1/chat/",
                        "/api/v1/profile/",
                        "/api/v1/home/slider/",
                        "/api/v1/home/containers/",
                    ],
                }
            }
        }
    )


def legacy_redirect_view(target: str, *, permanent: bool = True, status_code: int | None = None):
    """Return a view that redirects to `target`, preserving the query string."""

    code = status_code or (308 if permanent else 301)

    def _view(request, *args, **kwargs):
        url = target.format(**kwargs)
        if request.META.get("QUERY_STRING"):
            url = f"{url}?{request.META['QUERY_STRING']}"
        response = HttpResponsePermanentRedirect(url)
        response.status_code = code
        return response

    return _view
