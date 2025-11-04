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
<<<<<<< Updated upstream
                    "auth": [
                        "/api/v1/auth/login/",
                        "/api/v1/auth/logout/",
                        "/api/v1/auth/register/",
                        "/api/v1/auth/otp/send/",
                        "/api/v1/auth/oauth/google/",
                        "/api/v1/auth/oauth/facebook/",
=======
                    "resources": [
                        "/api/v1/auth/",
                        "/api/v1/categories/",
                        "/api/v1/services/",
                        "/api/v1/services/featured/",
                        "/api/v1/services/filters/",
                        "/api/v1/services/reactions/",
                        "/api/v1/profile/",
                        "/api/v1/profile/experience/",
                        "/api/v1/profile/studies/",
                        "/api/v1/profile/interests/",
                        "/api/v1/profile/certifications/",
                        "/api/v1/home/slider/",
                        "/api/v1/home/containers/",
                        "/api/v1/checkout/",
                        "/api/v1/checkout/webhook/",
                        "/api/v1/report/",
                        "/api/v1/trees/",
                        "/api/v1/chat/",
>>>>>>> Stashed changes
                    ],
                    "resources": {
                        "categories": "/api/v1/categories/",
                        "services": {
                            "base": "/api/v1/services/",
                            "filters": [
                                "/api/v1/services/filters/category/",
                                "/api/v1/services/filters/sub_category/",
                                "/api/v1/services/filters/city/",
                                "/api/v1/services/filters/state/",
                                "/api/v1/services/filters/country/",
                                "/api/v1/services/filters/comments/",
                                "/api/v1/services/filters/likes/",
                                "/api/v1/services/filters/dislikes/",
                            ],
                        },
                        "chat": "/api/v1/chat/",
                        "profile": {
                            "base": "/api/v1/profile/",
                            "sections": [
                                "/api/v1/profile/certifications/",
                                "/api/v1/profile/interests/",
                                "/api/v1/profile/studies/",
                                "/api/v1/profile/experience/",
                            ],
                        },
                        "home": [
                            "/api/v1/home/slider/",
                            "/api/v1/home/containers/",
                        ],
                        "checkout": "/api/v1/checkout/webhook",
                    },
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
